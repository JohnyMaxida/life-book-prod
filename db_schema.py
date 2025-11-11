"""
Database models for Life-Book bot using SQLAlchemy ORM.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, 
    Text, ForeignKey, JSON, Float, BigInteger, UniqueConstraint, Index
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func
# Using standard JSON for SQLite compatibility
# from sqlalchemy.dialects.postgresql import JSONB  # Removed for SQLite compatibility

# Use asyncpg for PostgreSQL or aiosqlite for SQLite
Base = declarative_base()

class UserRole(str, Enum):
    """User roles in the system."""
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class UserStatus(str, Enum):
    """User status in the marathon."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class MarathonDay(Base):
    """Tracks user progress for each day of the marathon."""
    __tablename__ = "marathon_days"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    day_number = Column(Integer, nullable=False)
    completed = Column(Boolean, default=False)
    completion_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    mood = Column(String(50), nullable=True)  # Could be an enum in a real implementation
    
    # Track completion of different tasks
    tasks_completed = Column(JSON, default=dict)  # {task_id: completion_status}
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="marathon_days")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'day_number', name='_user_day_uc'),
        Index('idx_marathon_days_user_day', 'user_id', 'day_number'),
    )
    
    def __repr__(self):
        return f"<MarathonDay(user_id={self.user_id}, day={self.day_number}, completed={self.completed})>"

class User(Base):
    """Main user model for the Life-Book bot."""
    __tablename__ = 'users'

    # Core identification
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True, index=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    language_code = Column(String(10), default='ru')
    nickname = Column(String(255), nullable=True, index=True)
    
    # Authentication & Status
    role = Column(String(20), default=UserRole.USER, nullable=False, index=True)
    status = Column(String(20), default=UserStatus.ACTIVE, nullable=False, index=True)
    is_bot = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)
    
    # Marathon progress
    current_day = Column(Integer, default=1, nullable=False)
    total_days = Column(Integer, default=28, nullable=False)
    streak_days = Column(Integer, default=0)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    
    # Stats & Points
    points = Column(Integer, default=0)  # General points (bales)
    lives = Column(Integer, default=3)   # Lives/attempts
    vitas = Column(Integer, default=0)   # Premium currency
    experience = Column(Integer, default=0)
    level = Column(Integer, default=1)
    
    # Time & Location
    timezone = Column(String(50), default='UTC+3')
    location = Column(String(100), nullable=True)
    
    # Referral system
    referral_code = Column(String(50), unique=True, nullable=True, index=True)
    referrer_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=True, index=True)
    referral_count = Column(Integer, default=0)
    referral_points = Column(Integer, default=0)
    
    # Payment & Subscription
    subscription_type = Column(String(50), default='free')
    subscription_ends = Column(DateTime, nullable=True)
    payment_id = Column(String(255), nullable=True, index=True)
    
    # User preferences
    settings = Column(JSON, default={
        'notifications': True,
        'daily_reminder': True,
        'weekly_summary': True,
        'theme': 'light',
        'language': 'ru',
    })
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    marathon_days = relationship("MarathonDay", back_populates="user", cascade="all, delete-orphan")
    
    # Self-referential relationship for referrals
    referrer = relationship(
        "User",
        remote_side=[user_id],  # This is the "remote" column in the parent/child relationship
        back_populates="referrals",
        foreign_keys=[referrer_id],
        post_update=True
    )
    
    referrals = relationship(
        "User",
        back_populates="referrer",
        foreign_keys=[referrer_id],
        lazy='select',
        post_update=True
    )
    
    # Indexes
    __table_args__ = (
        Index('idx_user_status', 'status'),
        Index('idx_user_role', 'role'),
        Index('idx_user_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
    
    @property
    def full_name(self) -> str:
        """Return the user's full name."""
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or 'Anonymous'
    
    @property
    def is_admin(self) -> bool:
        """Check if user has admin privileges."""
        return self.role in (UserRole.ADMIN, UserRole.SUPER_ADMIN)
    
    @property
    def is_moderator(self) -> bool:
        """Check if user has moderator privileges."""
        return self.role in (UserRole.MODERATOR, UserRole.ADMIN, UserRole.SUPER_ADMIN)
    
    @property
    def is_active(self) -> bool:
        """Check if user is active."""
        return self.status == UserStatus.ACTIVE
    
    def get_referral_link(self, bot_username: str) -> str:
        """Generate a referral link for the user."""
        if not self.referral_code:
            self.referral_code = f"ref_{self.user_id}_{hash(self.user_id) % 10000:04d}"
        return f"https://t.me/{bot_username}?start=ref{self.referral_code}"

# Additional models can be added here as needed
class UserActivityLog(Base):
    """Logs user activities for analytics and debugging."""
    __tablename__ = 'user_activity_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    action = Column(String(100), nullable=False)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    
    # Relationships
    user = relationship("User", backref="activity_logs")
    
    __table_args__ = (
        Index('idx_activity_user_action', 'user_id', 'action'),
        Index('idx_activity_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<UserActivityLog(user_id={self.user_id}, action='{self.action}')>"
