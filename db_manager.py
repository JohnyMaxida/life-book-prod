"""
Database manager for Life-Book bot using SQLAlchemy with async support.
"""
import logging
from typing import Optional, Dict, Any, List, Union
from datetime import datetime, timedelta

import asyncio
import time
from functools import wraps
from typing import Callable, TypeVar, Any, Optional

from sqlalchemy import select, update, delete, and_, or_, func, text
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import selectinload, joinedload

from db_schema import Base, User, UserRole, UserStatus, MarathonDay, UserActivityLog
from config import config

# Configure logging
logger = logging.getLogger(__name__)

T = TypeVar('T')

def retry_on_db_failure(
    max_retries: int = 3,
    initial_delay: float = 0.1,
    max_delay: float = 1.0,
    exceptions=(OperationalError, SQLAlchemyError)
):
    """Decorator for retrying database operations on failure."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:  # Don't sleep on the last attempt
                        jitter = 0.9 + 0.2 * (time.monotonic() % 1.0)  # Add some randomness
                        sleep_time = min(delay * jitter, max_delay)
                        await asyncio.sleep(sleep_time)
                        delay *= 2  # Exponential backoff
            
            # If we get here, all retries failed
            logger.error(f"Database operation failed after {max_retries} attempts")
            raise last_exception
        
        return wrapper
    return decorator

class DatabaseManager:
    """Manages database operations for the Life-Book bot with retry and health check support."""
    
    def __init__(self, database_url: str = None):
        """Initialize the database manager.
        
        Args:
            database_url: Database connection URL. If None, uses the one from config.
        """
        self.database_url = database_url or config.get('database_url', 'sqlite+aiosqlite:///./lifebook.db')
        self.engine: Optional[AsyncEngine] = None
        self.async_session = None
        self._is_healthy = False
        self._last_health_check = 0
        self.health_check_interval = 300  # 5 minutes between health checks
    
    async def init_db(self) -> None:
        """Initialize the database connection and create tables."""
        logger.info(f"Initializing database: {self.database_url}")
        
        try:
            # Create async engine with connection pooling
            self.engine = create_async_engine(
                self.database_url,
                echo=config.get('debug', False),
                pool_pre_ping=True,
                pool_recycle=3600,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                connect_args={"timeout": 30, "check_same_thread": False} if "sqlite" in self.database_url else {"timeout": 30}
            )
            
            # Test connection
            await self._test_connection()
            
            # Create async session factory
            self.async_session = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=True
            )
            
            # Create tables if they don't exist
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            # Mark as healthy
            self._is_healthy = True
            self._last_health_check = time.time()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            self._is_healthy = False
            raise
    
    async def _test_connection(self) -> None:
        """Test the database connection with a simple query."""
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            raise
    
    async def check_health(self, force: bool = False) -> bool:
        """Check if the database connection is healthy.
        
        Args:
            force: If True, force a health check even if recently checked.
            
        Returns:
            bool: True if healthy, False otherwise
        """
        current_time = time.time()
        
        # Skip if we've checked recently and are healthy
        if not force and self._is_healthy and \
           (current_time - self._last_health_check) < self.health_check_interval:
            return True
            
        try:
            await self._test_connection()
            self._is_healthy = True
        except Exception as e:
            logger.warning(f"Database health check failed: {e}")
            self._is_healthy = False
            
        self._last_health_check = current_time
        return self._is_healthy
    
    # User management
    @retry_on_db_failure()
    async def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by their Telegram ID.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            User object if found, None otherwise
            
        Raises:
            SQLAlchemyError: If there's a database error after retries
        """
        async with self.async_session() as session:
            try:
                result = await session.execute(
                    select(User)
                    .options(selectinload(User.marathon_days))
                    .where(User.user_id == user_id)
                )
                return result.scalar_one_or_none()
            except Exception as e:
                logger.error(f"Error in get_user for user_id={user_id}: {e}")
                raise
    
    @retry_on_db_failure()
    async def get_or_create_user(
        self,
        user_id: int,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        language_code: str = 'ru',
        nickname: str = None,
        **extra_fields
    ) -> User:
        """Get a user or create if not exists.
        
        Args:
            user_id: Telegram user ID
            username: Telegram username (optional)
            first_name: User's first name (optional)
            last_name: User's last name (optional)
            language_code: User's language code (default: 'ru')
            nickname: User's nickname (optional)
            **extra_fields: Additional fields to set on the user
            
        Returns:
            User object (existing or newly created)
            
        Raises:
            SQLAlchemyError: If there's a database error after retries
        """
        async with self.async_session() as session:
            try:
                # Try to get existing user
                result = await session.execute(
                    select(User).where(User.user_id == user_id)
                )
                user = result.scalar_one_or_none()
                
                # Create new user if not exists
                if not user:
                    user = User(
                        user_id=user_id,
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        language_code=language_code,
                        nickname=nickname or f"user_{user_id}",
                        role=UserRole.USER,
                        status=UserStatus.ACTIVE,
                        current_day=1,
                        total_days=28,
                        lives=3,
                        timezone='UTC+3',
                        settings={
                            'notifications': True,
                            'language': language_code or 'ru',
                            'timezone': 'UTC+3',
                            'theme': 'light',
                            'daily_reminder': True,
                            'progress_notifications': True,
                        },
                        **extra_fields
                    )
                    session.add(user)
                    await session.commit()
                    logger.info(f"Created new user: {user_id} ({nickname or username or 'no-username'})")
                
                return user
                
            except Exception as e:
                await session.rollback()
                logger.error(f"Error in get_or_create_user for user_id={user_id}: {e}")
                raise
            
            return user
    
    async def update_user(
        self,
        user_id: int,
        **updates
    ) -> Optional[User]:
        """Update user fields."""
        async with self.async_session() as session:
            result = await session.execute(
                update(User)
                .where(User.user_id == user_id)
                .values(**updates)
                .returning(User)
            )
            await session.commit()
            return result.scalar_one_or_none()
    
    async def delete_user(self, user_id: int) -> bool:
        """Delete a user by their ID."""
        async with self.async_session() as session:
            result = await session.execute(
                delete(User).where(User.user_id == user_id)
            )
            await session.commit()
            return result.rowcount > 0
    
    # Marathon progress
    async def get_user_day(self, user_id: int) -> int:
        """Get the current day for a user."""
        user = await self.get_user(user_id)
        return user.current_day if user else 1
    
    async def set_user_day(self, user_id: int, day: int) -> bool:
        """Set the current day for a user."""
        result = await self.update_user(user_id, current_day=day)
        return result is not None
    
    async def complete_day(self, user_id: int, day: int, notes: str = None) -> bool:
        """Mark a day as completed for a user."""
        async with self.async_session() as session:
            # Check if day is already completed
            result = await session.execute(
                select(MarathonDay)
                .where(and_(
                    MarathonDay.user_id == user_id,
                    MarathonDay.day_number == day
                ))
            )
            marathon_day = result.scalar_one_or_none()
            
            if marathon_day:
                # Update existing day
                marathon_day.completed = True
                marathon_day.completion_date = datetime.utcnow()
                if notes:
                    marathon_day.notes = notes
            else:
                # Create new completed day
                marathon_day = MarathonDay(
                    user_id=user_id,
                    day_number=day,
                    completed=True,
                    completion_date=datetime.utcnow(),
                    notes=notes
                )
                session.add(marathon_day)
            
            # Update user's current day if needed
            user = await self.get_user(user_id)
            if user and user.current_day <= day and day < user.total_days:
                user.current_day = day + 1
                user.streak_days += 1
                user.points += 10  # Award points for completing a day
            
            await session.commit()
            return True
    
    # Points and rewards
    async def update_points(
        self,
        user_id: int,
        points_delta: int = 0,
        lives_delta: int = 0,
        vitas_delta: int = 0
    ) -> Dict[str, int]:
        """Update user's points, lives, and vitas."""
        async with self.async_session() as session:
            result = await session.execute(
                select(User)
                .where(User.user_id == user_id)
                .with_for_update()
            )
            user = result.scalar_one_or_none()
            
            if not user:
                return {"points": 0, "lives": 0, "vitas": 0}
            
            # Update values
            user.points = max(0, user.points + points_delta)
            user.lives = max(0, user.lives + lives_delta)
            user.vitas = max(0, user.vitas + vitas_delta)
            
            # Check for level up
            exp_needed = user.level * 100
            if user.experience >= exp_needed:
                user.level += 1
                user.experience = 0
                logger.info(f"User {user_id} leveled up to {user.level}")
            
            await session.commit()
            
            return {
                "points": user.points,
                "lives": user.lives,
                "vitas": user.vitas,
                "level": user.level,
                "experience": user.experience
            }
    
    # Referral system
    async def add_referral(self, referrer_id: int, referred_id: int) -> bool:
        """Add a referral relationship between users."""
        async with self.async_session() as session:
            # Check if users exist and aren't the same
            if referrer_id == referred_id:
                return False
                
            referrer = await self.get_user(referrer_id)
            referred = await self.get_user(referred_id)
            
            if not referrer or not referred or referred.referrer_id:
                return False
            
            # Update referred user's referrer
            referred.referrer_id = referrer_id
            
            # Update referrer's stats
            referrer.referral_count += 1
            referrer.referral_points += 10  # Award points for referral
            
            # Award bonus for multiple referrals
            if referrer.referral_count % 5 == 0:
                referrer.vitas += 1
                logger.info(f"User {referrer_id} earned a vita for 5 referrals")
            
            await session.commit()
            return True
    
    # Activity logging
    async def log_activity(
        self,
        user_id: int,
        action: str,
        details: Dict[str, Any] = None,
        ip_address: str = None,
        user_agent: str = None
    ) -> None:
        """Log user activity."""
        async with self.async_session() as session:
            log = UserActivityLog(
                user_id=user_id,
                action=action,
                details=details or {},
                ip_address=ip_address,
                user_agent=user_agent
            )
            session.add(log)
            await session.commit()
    
    # Admin functions
    async def get_all_users(
        self,
        skip: int = 0,
        limit: int = 100,
        role: str = None,
        status: str = None
    ) -> List[User]:
        """Get a list of users with optional filtering."""
        async with self.async_session() as session:
            query = select(User)
            
            if role:
                query = query.where(User.role == role)
            if status:
                query = query.where(User.status == status)
            
            result = await session.execute(
                query.order_by(User.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            return list(result.scalars())
    
    async def search_users(
        self,
        query: str,
        limit: int = 20
    ) -> List[User]:
        """Search users by username, first name, or last name."""
        if not query or len(query) < 2:
            return []
            
        search = f"%{query}%"
        async with self.async_session() as session:
            result = await session.execute(
                select(User)
                .where(or_(
                    User.username.ilike(search),
                    User.first_name.ilike(search),
                    User.last_name.ilike(search)
                ))
                .limit(limit)
            )
            return list(result.scalars())
    
    @retry_on_db_failure()
    async def get_user_by_referral_code(self, referral_code: str) -> Optional[User]:
        """Get a user by their referral code."""
        async with self.async_session() as session:
            try:
                result = await session.execute(
                    select(User).where(User.referral_code == referral_code)
                )
                return result.scalar_one_or_none()
            except Exception as e:
                logger.error(f"Error in get_user_by_referral_code for code={referral_code}: {e}")
                raise
    
    # Statistics
    async def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get detailed statistics for a user."""
        async with self.async_session() as session:
            # Get user and completed days
            user = await self.get_user(user_id)
            if not user:
                return {}
            
            # Count completed days
            result = await session.execute(
                select(func.count(MarathonDay.id))
                .where(and_(
                    MarathonDay.user_id == user_id,
                    MarathonDay.completed == True
                ))
            )
            completed_days = result.scalar() or 0
            
            # Calculate streak
            result = await session.execute(
                select(MarathonDay)
                .where(and_(
                    MarathonDay.user_id == user_id,
                    MarathonDay.completed == True
                ))
                .order_by(MarathonDay.day_number.desc())
            )
            completed_days_list = [day.day_number for day in result.scalars()]
            
            streak = 0
            expected_day = user.current_day - 1
            while expected_day in completed_days_list:
                streak += 1
                expected_day -= 1
            
            return {
                "user_id": user.user_id,
                "username": user.username,
                "full_name": user.full_name,
                "level": user.level,
                "experience": user.experience,
                "points": user.points,
                "lives": user.lives,
                "vitas": user.vitas,
                "current_day": user.current_day,
                "total_days": user.total_days,
                "completed_days": completed_days,
                "completion_percentage": int((completed_days / user.total_days) * 100) if user.total_days > 0 else 0,
                "streak_days": user.streak_days,
                "referral_count": user.referral_count,
                "referral_points": user.referral_points,
                "created_at": user.created_at,
                "last_active": user.last_active
            }

# Global database manager instance
_db = None

async def get_db() -> DatabaseManager:
    """
    Get the database manager instance, initializing it if necessary.
    
    Returns:
        DatabaseManager: Initialized database manager instance
        
    Raises:
        RuntimeError: If database initialization fails
    """
    global _db
    if _db is None:
        _db = DatabaseManager()
        try:
            await _db.init_db()
            logger.info("Database manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            _db = None
            raise RuntimeError("Failed to initialize database") from e
    return _db

# The database initialization is now handled in lifebook.py
