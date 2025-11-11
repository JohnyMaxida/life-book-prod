"""
New LIFEMAN module with improved database structure.
Maintains backward compatibility with existing code.
"""
import json
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
# from lifebook import LIFE_DB_file # This import seems problematic, LIFE_DB_file is not defined in lifebook.py
from db_manager import DBManager, get_db # Import get_db to get the DatabaseManager instance
from logger import logger # Import logger

# Database file path will be set by DBManager
DB_PATH = None # This will be managed by DBManager

# Database connection will be managed by get_db()
# No need for global db variable anymore

async def initialize_lifeman_db():
    """Initialize the database connection for lifeman.
    
    Note: This function is kept for backward compatibility but doesn't do anything
    since the database is now managed by get_db().
    """
    logger.info("Lifeman database initialized.")

# Constants
BOGDAN_URL = "https://t.me/Bodyagolos"
DONNA_URL = "https://t.me/donnaaibot?start=ref1315"
UNILIV_URL = "https://h.heigu.top//#/login?recomId=gVRYv2&language=ru_RU"
AXIOM5_URL = "https://t.me/five_live_axioma_bot?start=3aRlaBk"
AXIOM_REF = 'Bodyagolos'
AXIOM_URL = 'https://t.me/axiomeru/486'

def _get_affiliate_link(user_data: dict, link_key: str) -> str:
    """Safely extract an affiliate link from user data.
    
    Args:
        user_data: The user data dictionary
        link_key: The key of the affiliate link to get (e.g., 'donna', 'uni')
        
    Returns:
        str: The affiliate link or empty string if not found
    """
    if not user_data:
        return ''
        
    affiliate_links = user_data.get('affiliate_links', {})
    
    # If affiliate_links is a string, try to parse it as JSON
    if isinstance(affiliate_links, str):
        try:
            affiliate_links = json.loads(affiliate_links)
        except (json.JSONDecodeError, TypeError):
            # If it's not valid JSON, check if it's a direct URL for the requested key
            if link_key == 'donna' and 'donna' in affiliate_links.lower():
                return affiliate_links
            return ''
    
    # If we have a dictionary, get the link by key
    if isinstance(affiliate_links, dict):
        return affiliate_links.get(link_key, '')
        
    return ''

# User management
async def Check_User(user_id: int) -> Optional[Dict[str, Any]]:
    """Check if user exists and return their data."""
    if db is None:
        await initialize_lifeman_db()
    
    user = await db.get_user(user_id)
    if not user:
        return None
    
    # Prepare user data with values from the User model
    user_data = {
        'user_name': user.username,
        'user_nick': user.nickname,
        'day': user.current_day,
        'user_stime': user.start_date,  # Assuming user_stime maps to start_date
        'user_work': user.points, # Assuming user_work maps to points or similar
        'Lives': user.lives,
        'Vitas': user.vitas,
        'Antes': 0, # No direct mapping, default to 0
        'Doles': 0, # No direct mapping, default to 0
        'pay_status': 0, # No direct mapping, default to 0
        'user_role': user.role,
        'user_rate': user.level, # Assuming user_rate maps to level
        'user_tz': user.timezone, # Assuming user_tz maps to timezone
        'user_dole_FP': False, # No direct mapping, default to False
        'user_donna_FP': False, # No direct mapping, default to False
        # Handle affiliate_links whether it's a string or dict
        'user_donna_url': _get_affiliate_link(user, 'donna'),
        'user_uni_url': _get_affiliate_link(user, 'uni'),
        'user_axi0_url': _get_affiliate_link(user, 'axi0'),
        'user_axi5_url': _get_affiliate_link(user, 'axi5')
    }
    
    return user_data

async def Reg_User(user_id: int, username: str, first_name: str, last_name: str, nickname: str) -> bool:
    """Register a new user in the database."""
    if db is None:
        await initialize_lifeman_db()
        
    # Use get_or_create_user from db_manager to handle creation and defaults
    user = await db.get_or_create_user(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        nickname=nickname,
        # Additional fields can be passed here if needed
        # For example, if you want to set initial affiliate links during creation
        # affiliate_links={
        #     'donna': DONNA_URL,
        #     'uni': UNILIV_URL,
        #     'axi0': AXIOM_REF,
        #     'axi5': AXIOM5_URL
        # }
    )
    
    return user is not None

# Field accessors
async def Get_DOLE_FP(user_id: int) -> Optional[bool]:
    """Get user_dole_FP value."""
    if db is None:
        await initialize_lifeman_db()
    # Assuming 'user_dole_FP' is a field in the User model or settings JSON
    user = await db.get_user(user_id)
    return user.settings.get('user_dole_FP', False) if user and user.settings else False

async def Set_DOLE_FP(user_id: int, value: bool) -> bool:
    """Set user_dole_FP value."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    if user:
        settings = user.settings
        settings['user_dole_FP'] = value
        return await db.update_user(user_id, settings=settings) is not None
    return False

async def Get_DONNA_FP(user_id: int) -> Optional[bool]:
    """Get user_donna_FP value."""
    if db is None:
        await initialize_lifeman_db()
    # Assuming 'user_donna_FP' is a field in the User model or settings JSON
    user = await db.get_user(user_id)
    return user.settings.get('user_donna_FP', False) if user and user.settings else False

async def Set_DONNA_FP(user_id: int, value: bool) -> bool:
    """Set user_donna_FP value."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    if user:
        settings = user.settings
        settings['user_donna_FP'] = value
        return await db.update_user(user_id, settings=settings) is not None
    return False

async def Get_Afilink(link_index: int, user_id: int) -> str:
    if db is None:
        await initialize_lifeman_db()
    # Assuming affiliate links are stored in user.settings or a dedicated field
    user = await db.get_user(user_id)
    if user and user.settings and 'affiliate_links' in user.settings:
        links = user.settings['affiliate_links']
        link_keys = {1: 'donna', 2: 'uni', 3: 'axi0', 4: 'axi5'}
        return links.get(link_keys.get(link_index, ''), '')
    return ''

async def Set_Afilink(link_index: int, url: str, user_id: int) -> bool:
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    if user:
        settings = user.settings
        if 'affiliate_links' not in settings:
            settings['affiliate_links'] = {}
        link_keys = {1: 'donna', 2: 'uni', 3: 'axi0', 4: 'axi5'}
        settings['affiliate_links'][link_keys.get(link_index, '')] = url
        return await db.update_user(user_id, settings=settings) is not None
    return False

# User data accessors
async def get_rate(user_id: int) -> Optional[int]:
    """Get user_rating value."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    return user.level if user else None # Assuming user_rating maps to level

async def get_pays(user_id: int) -> Optional[int]:
    """Get pay_status value."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    # Assuming pay_status is derived from subscription_type or a dedicated field
    return 1 if user and user.subscription_type != 'free' else 0

async def get_role(user_id: int) -> Optional[str]:
    """Get user_role value."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    return user.role if user else None

async def get_ref_count(user_id: int) -> Optional[int]:
    """Get referral_count value."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    return user.referral_count if user else None

async def get_ref_code(user_id: int) -> Optional[str]:
    """Get referral_code value."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    return user.referral_code if user else None

async def get_day(user_id: int) -> Optional[int]:
    """Get day value."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    return user.current_day if user else None

async def getdb_time(user_id: int) -> str:
    """Get user_stime value as a properly formatted string for S2TIME."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    time_val = user.start_date if user else None # Assuming user_stime maps to start_date
    
    # If it's already a datetime object, format it
    if isinstance(time_val, datetime):
        return time_val.strftime('%Y-%m-%d %H:%M')
        
    # If it's a string, ensure it's in the correct format
    if isinstance(time_val, str):
        try:
            # Try to parse and reformat to ensure consistency
            dt = datetime.strptime(time_val, '%Y-%m-%d %H:%M')
            return dt.strftime('%Y-%m-%d %H:%M')
        except (ValueError, TypeError):
            # If parsing fails, try to extract time components
            import re
            time_match = re.search(r'(\d{1,2})[:.-](\d{1,2})', str(time_val))
            if time_match:
                hours, minutes = map(int, time_match.groups())
                now = datetime.now()
                return now.replace(hour=hours, minute=minutes).strftime('%Y-%m-%d %H:%M')
            
    # If all else fails, return current time
    return datetime.now().strftime('%Y-%m-%d %H:%M')

async def get_uwork(user_id: int) -> Optional[int]:
    """Get user_work value."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    return user.points if user else None # Assuming user_work maps to points

async def get_timezone(user_id: int) -> Optional[str]: # Changed return type to str as per db_schema
    """Get user_timezone value."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    return user.timezone if user else None

async def get_credos(user_id: int, crendex: int) -> Optional[int]:
    """Get credential value by index."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    if not user:
        return None
    cred_map = {1: 'lives', 2: 'vitas', 3: 'Antes', 4: 'Doles'} # Use lowercase for lives/vitas
    field = cred_map.get(crendex)
    if field == 'lives':
        return user.lives
    elif field == 'vitas':
        return user.vitas
    # For 'Antes' and 'Doles', assuming they might be in settings or not directly mapped
    return user.settings.get(field) if user.settings and field in user.settings else None

# User data setters
async def save_role(user_id: int, role: str) -> bool:
    """Set user_role value."""
    if db is None:
        await initialize_lifeman_db()
    return await db.update_user(user_id, role=role) is not None

async def save_rate(user_id: int, rate: int) -> bool:
    """Set user_rating value."""
    if db is None:
        await initialize_lifeman_db()
    return await db.update_user(user_id, level=rate) is not None # Assuming user_rating maps to level

async def save_pays(user_id: int, pays: int) -> bool:
    """Set pay_status value."""
    if db is None:
        await initialize_lifeman_db()
    # Assuming pays maps to subscription_type
    subscription_type = 'premium' if pays == 1 else 'free'
    return await db.update_user(user_id, subscription_type=subscription_type) is not None

async def save_day(user_id: int, day: int) -> bool:
    """Set day value."""
    if db is None:
        await initialize_lifeman_db()
    return await db.update_user(user_id, current_day=day) is not None

async def savedb_time(user_id: int, time_val: Union[datetime, str, None]) -> bool:
    """Set user_stime value with proper formatting.
    
    Args:
        time_val: Can be datetime object, string in various formats, or None
        
    Returns:
        bool: True if save was successful, False otherwise
    """
    if db is None:
        await initialize_lifeman_db()
        
    processed_time = None
    
    # Handle datetime objects
    if isinstance(time_val, datetime):
        processed_time = time_val
    # Handle strings
    elif isinstance(time_val, str):
        try:
            # Try to parse as full datetime
            processed_time = datetime.strptime(time_val, '%Y-%m-%d %H:%M')
        except ValueError:
            try:
                # Try to parse as time only (HH:MM)
                from datetime import time as dt_time
                t = dt_time.fromisoformat(time_val)
                now = datetime.now()
                processed_time = now.replace(
                    hour=t.hour, 
                    minute=t.minute, 
                    second=0, 
                    microsecond=0
                )
            except (ValueError, AttributeError):
                # If parsing fails, use current time
                processed_time = datetime.now()
    
    # If we couldn't process the time, use current time
    if processed_time is None:
        processed_time = datetime.now()
    
    # Save the processed time
    return await db.update_user(user_id, start_date=processed_time) is not None # Assuming user_stime maps to start_date

async def save_uwork(user_id: int, user_work: int) -> bool:
    """Set user_work value."""
    if db is None:
        await initialize_lifeman_db()
    return await db.update_user(user_id, points=user_work) is not None # Assuming user_work maps to points

async def save_timezone(user_id: int, timezone: str) -> bool: # Changed timezone type to str
    """Set user_timezone value."""
    if db is None:
        await initialize_lifeman_db()
    return await db.update_user(user_id, timezone=timezone) is not None

async def save_credos(user_id: int, crendex: int, value: int) -> bool:
    """Set credential value by index."""
    if db is None:
        await initialize_lifeman_db()
    cred_map = {1: 'lives', 2: 'vitas', 3: 'Antes', 4: 'Doles'}
    field = cred_map.get(crendex)
    if field == 'lives':
        return await db.update_user(user_id, lives=value) is not None
    elif field == 'vitas':
        return await db.update_user(user_id, vitas=value) is not None
    # For 'Antes' and 'Doles', assuming they might be in settings
    user = await db.get_user(user_id)
    if user:
        settings = user.settings
        settings[field] = value
        return await db.update_user(user_id, settings=settings) is not None
    return False

# User answers
async def Set_user_responses(user_id: int, responses: dict) -> bool:
    """Save user responses to the database."""
    if db is None:
        await initialize_lifeman_db()
    # Assuming responses are stored in user.settings or a dedicated field
    user = await db.get_user(user_id)
    if user:
        settings = user.settings
        settings['responses'] = responses
        return await db.update_user(user_id, settings=settings) is not None
    return False

async def Get_user_responses(user_id: int) -> Dict[str, Any]:
    """Get user responses from the database."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    return user.settings.get('responses', {}) if user and user.settings else {}

async def delete_user_responses(user_id: int) -> bool:
    """Delete user responses from the database."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    if user:
        settings = user.settings
        if 'responses' in settings:
            del settings['responses']
            return await db.update_user(user_id, settings=settings) is not None
    return False

# Referral system
async def Process_Relink(user_id: int, start_parameter: str) -> None:
    """Process a referral link."""
    # Implementation depends on your referral system
    logger.info(f"Processing referral link for user {user_id} with parameter {start_parameter}")
    pass

async def Update_Referrer(referrer_id: int, referred_id: int) -> bool:
    """Update referrer statistics."""
    if db is None:
        await initialize_lifeman_db()
    return await db.add_referral(referrer_id, referred_id)

async def Generate_Ref_Code(user_id: int) -> str:
    """Generate a unique referral code."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    if user and not user.referral_code:
        # Generate a simple referral code for now, can be improved
        referral_code = f"ref_{user_id}"
        await db.update_user(user_id, referral_code=referral_code)
        return referral_code
    return user.referral_code if user else ""

# New functions for marathon_logic
async def get_uweek(user_id: int) -> Optional[int]:
    """Get user's current week."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    # Assuming 'current_week' is a field in the User model or settings JSON
    return user.settings.get('current_week', 1) if user and user.settings else 1

async def save_uweek(user_id: int, week: int) -> bool:
    """Set user's current week."""
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    if user:
        settings = user.settings
        settings['current_week'] = week
        return await db.update_user(user_id, settings=settings) is not None
    return False

async def Inc_Lives(user_id: int, lives: int = 1) -> bool:
    """Increment user's lives."""
    if db is None:
        await initialize_lifeman_db()
    result = await db.update_points(user_id, lives_delta=lives)
    return result is not None

async def Inc_Vitas(user_id: int, vitas: int = 1) -> bool:
    """Increment user's vitas."""
    if db is None:
        await initialize_lifeman_db()
    result = await db.update_points(user_id, vitas_delta=vitas)
    return result is not None

# Backward compatibility functions removed as part of aiogram 3.x migration.
# These functions should be replaced with direct calls to the refactored lifeman functions.

# Affiliate link accessors (updated to use new Get_Afilink/Set_Afilink)
async def Get_DONNA_URL(user_id: int) -> str:
    return await Get_Afilink(1, user_id)
async def Set_DONNA_URL(user_id: int, url: str) -> bool:
    return await Set_Afilink(1, url, user_id)
async def Get_UNI_URL(user_id: int) -> str:
    return await Get_Afilink(2, user_id)
async def Set_UNI_URL(user_id: int, url: str) -> bool:
    return await Set_Afilink(2, url, user_id)
async def Get_AXI0M_REF(user_id: int) -> str:
    return await Get_Afilink(3, user_id)
async def Set_AXI0M_REF(user_id: int, url: str) -> bool:
    return await Set_Afilink(3, url, user_id)
async def Get_AXI5M_URL(user_id: int) -> str:
    return await Get_Afilink(4, user_id)
async def Set_AXI5M_URL(user_id: int, url: str) -> bool:
    return await Set_Afilink(4, url, user_id)

# Other compatibility functions that need to be updated or removed
async def Get_uid_day(user_id: int) -> Optional[int]:
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    return user.current_day if user else None

async def Get_user_info(user_id: int) -> Optional[Dict[str, Any]]:
    if db is None:
        await initialize_lifeman_db()
    return await db.get_user(user_id)

async def Get_user_full(user_id: int) -> Optional[Dict[str, Any]]:
    if db is None:
        await initialize_lifeman_db()
    return await db.get_user(user_id)

async def get_users_count() -> int:
    if db is None:
        await initialize_lifeman_db()
    return await db.get_users_count()

async def print_users_limit(offset: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
    if db is None:
        await initialize_lifeman_db()
    # This function returns User objects, not dicts. Conversion might be needed.
    users = await db.get_all_users(skip=offset, limit=limit)
    return [user.__dict__ for user in users] # Convert to dict for compatibility

async def delete_user(user_id: int) -> bool:
    if db is None:
        await initialize_lifeman_db()
    return await db.delete_user(user_id)

async def Get_Ref_Lives(ref_id: int) -> Optional[int]:
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(ref_id)
    return user.lives if user else None

async def Update_Ref_Lives(ref_id: int, lives: int) -> bool:
    if db is None:
        await initialize_lifeman_db()
    return await db.update_user(ref_id, lives=lives) is not None

async def Get_Ref_Vitas(ref_id: int) -> Optional[int]:
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(ref_id)
    return user.vitas if user else None

async def Update_Ref_Vitas(ref_id: int, vitas: int) -> bool:
    if db is None:
        await initialize_lifeman_db()
    return await db.update_user(ref_id, vitas=vitas) is not None

async def Update_Ref_Status(ref_id: int, status: str) -> bool:
    if db is None:
        await initialize_lifeman_db()
    return await db.update_user(ref_id, status=status) is not None

async def Get_Refer_Data(user_id: int) -> Dict[str, Any]:
    if db is None:
        await initialize_lifeman_db()
    user = await db.get_user(user_id)
    if user:
        return {
            "referral_count": user.referral_count,
            "referral_points": user.referral_points,
            "referrer_id": user.referrer_id
        }
    return {}

async def Calc_Bonus(ref_id: int) -> Dict[str, Any]:
    if db is None:
        await initialize_lifeman_db()
    # This function's logic is not directly mapped to db_manager.
    # It might need to be re-implemented based on business logic.
    # For now, return a placeholder.
    logger.info(f"Calculating bonus for referrer {ref_id} (placeholder)")
    return {"bonus_points": 0, "bonus_vitas": 0}
