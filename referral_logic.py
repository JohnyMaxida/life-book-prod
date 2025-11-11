"""
Логика реферальной системы: обработка ссылок, начисление бонусов.
"""

from datetime import datetime
from typing import Dict, Any, Optional, List

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from lifeman import (
    get_ref_code, get_ref_count, get_credos, save_credos, save_role, get_role,
    Get_DONNA_URL, Set_DONNA_URL, Get_UNI_URL, Set_UNI_URL,
    Get_AXI0M_REF, Set_AXI0M_REF, Get_AXI5M_URL, Set_AXI5M_URL,
    Update_Referrer, Generate_Ref_Code, Get_Refer_Data, Calc_Bonus,
    Inc_Lives, Inc_Vitas # Assuming these are the canonical ones
)
from db_manager import DatabaseManager, get_db # Use the initialized db_manager instance
from logger import logger # Centralized logger
from const import DONNA_URL, UNILIV_URL, AXIOM5_URL, AXIOM_REF, AXIOM_URL # Import constants
from utils import pluralize_ru # Only keep necessary utility functions

# Initialize logger
logger = logger.getLogger(__name__)

async def Comb_Reflink(bot_username: str, code: str) -> str:
    """Combines the bot username with a referral code to create a full referral link."""
    return f"https://t.me/{bot_username}?start={code}"

# The wrapper functions for Get/Set_DONNA_URL, Get/Set_UNI_URL, etc. are removed.
# Direct calls to lifeman functions will be used, passing user_id explicitly.

# The wrapper functions for get_ref_code and get_ref_count are removed.
# Direct calls to lifeman functions will be used, passing user_id explicitly.

async def Get_Ref_Lives(user_id: int) -> Optional[int]:
    """Get Lives value for a specific user."""
    return await get_credos(user_id, 1) # Assuming 1 is for Lives

async def Update_Ref_Lives(user_id: int, lives: int) -> bool:
    """Update Lives value for a specific user."""
    return await save_credos(user_id, 1, lives)

async def Get_Ref_Vitas(user_id: int) -> Optional[int]:
    """Get Vitas value for a specific user."""
    return await get_credos(user_id, 2) # Assuming 2 is for Vitas

async def Update_Ref_Vitas(user_id: int, vitas: int) -> bool:
    """Update Vitas value for a specific user."""
    return await save_credos(user_id, 2, vitas)

async def Update_Ref_Status(user_id: int, status: str) -> bool:
    """Update user status."""
    # Assuming 'status' is a field in the User model
    db_manager = await get_db()
    return await db_manager.update_user(user_id, status=status) is not None

async def Process_Relink(start_parameter: str, user_id: int, db_manager: DatabaseManager) -> Dict[str, Any]:
    """Process a referral link activation."""
    logger.info(f"Processing referral link for user {user_id} with parameter {start_parameter}")
    try:
        # Extract referrer_id from start_parameter
        # Assuming start_parameter is in format 'ref<referrer_id>' or 'ref_<referrer_id>'
        if start_parameter.startswith('ref'):
            referrer_code = start_parameter[3:]
            # Need to find referrer_id by referral_code
            referrer_user = await db_manager.get_user_by_referral_code(referrer_code) # Assuming this method exists
            if not referrer_user:
                return {'success': False, 'error': 'Referrer not found'}
            referrer_id = referrer_user.user_id
        else:
            return {'success': False, 'error': 'Invalid referral parameter format'}

        if referrer_id == user_id:
            logger.info("Detected self-referral.")
            return {'success': False, 'error': 'Opened own referral link'}
        
        # Check if referral record already exists
        user = await db_manager.get_user(user_id)
        if user and user.referrer_id:
            logger.info("Referral record already exists, skipping.")
            return {'success': False, 'error': 'Referral record already exists'}

        # Add referral relationship
        success = await db_manager.add_referral(referrer_id, user_id)
        
        if success:
            referrer_info = await db_manager.get_user(referrer_id)
            return {
                'success': True,
                'referrer_id': referrer_id,
                'user_name': referrer_info.username,
                'referral_count': referrer_info.referral_count,
                'lives': referrer_info.lives
            }
        else:
            return {'success': False, 'error': 'Error adding referral'}
            
    except Exception as e:
        logger.error(f"Error in Process_Relink: {e}")
        return {'success': False, 'error': str(e)}

# Update_Referrer is now handled by db_manager.add_referral

async def Get_Refer_Data(user_id: int, db_manager: DatabaseManager) -> List[Dict[str, Any]]:
    """Get referral data for a specific user."""
    logger.info(f"Getting referral matrix for user: {user_id}")
    # This needs to be implemented using db_manager methods to query referral relationships
    # For now, return a placeholder
    return []

async def Calc_Bonus(user_id: int, db_manager: DatabaseManager) -> Dict[str, Any]:
    """Calculate referral bonus based on direct and second-level referrals."""
    logger.info(f"Calculating referral coefficient for user {user_id}")
    # This function's logic needs to be re-implemented using db_manager methods.
    # For now, return a placeholder.
    return {"bonus_points": 0, "bonus_vitas": 0}

# Functions from active.py (Inc_ref_Bales, Inc_ref_Lives) are removed as they are duplicates
# and their logic should be handled by lifeman.Inc_Lives/Inc_Vitas and message sending in handlers.

async def process_referral_flow(message: Message, state: FSMContext, db_manager: DatabaseManager) -> Optional[int]:
    """Handles the referral processing flow for a new user."""
    user_id = message.from_user.id
    start_parameter = (await state.get_data()).get('start_param') # Get start_param from FSMContext
    
    if not start_parameter:
        return None

    result = await Process_Relink(start_parameter, user_id, db_manager)
    if not result.get('success'):
        return None

    referrer_id = result['referrer_id']
    new_user_name = message.from_user.full_name # Use full_name from Message

    # Copy affiliate links from referrer
    await Set_DONNA_URL(user_id, await Get_DONNA_URL(referrer_id))
    await Set_UNI_URL(user_id, await Get_UNI_URL(referrer_id))
    await Set_AXI0M_REF(user_id, await Get_AXI0M_REF(referrer_id))
    await Set_AXI5M_URL(user_id, await Get_AXI5M_URL(referrer_id))

    # Notify referrer (assuming bot object is available or passed)
    # This part needs the Bot instance to send messages
    bot = message.bot
    notify_text = (
        f"🎉 По вашей ссылке присоединился: {new_user_name}\n"
        f"Всего рефералов: {result['referral_count']}"
    )
    await bot.send_message(referrer_id, notify_text)

    # Award bonus (using lifeman.Inc_Lives/Inc_Vitas)
    await Inc_Lives(referrer_id, 1) # Example: award 1 life for referral
    
    return referrer_id


async def update_referral_data_flow(user_id: int, state: FSMContext, db_manager: DatabaseManager) -> None:
    """Updates referral data in FSMContext."""
    ref_code = await get_ref_code(user_id)
    if not ref_code:
        ref_code = await Generate_Ref_Code(user_id) # Generate if not exists
        
    bot_info = await (await get_db()).get_bot_info() # Assuming db_manager can get bot info
    bot_username = bot_info.username if bot_info else "LifeBookBot" # Placeholder
    
    ref_link = await Comb_Reflink(bot_username, ref_code)
    ref_count = await get_ref_count(user_id)

    await state.update_data(user_refcode=ref_code, user_reflink=ref_link, ref_count=ref_count)


async def handle_referral_menu(message: Message, state: FSMContext, db_manager: DatabaseManager) -> None:
    """Displays the referral program menu."""
    await update_referral_data_flow(message.from_user.id, state, db_manager)
    user_data = await state.get_data()
    
    ref_code = user_data.get('user_refcode', 'N/A')
    ref_link = user_data.get('user_reflink', 'N/A')
    ref_count = user_data.get('ref_count', 0)

    text = (
        f"🤝 *Реферальная программа*\n\n"
        f"Ваш код: `{ref_code}`\n"
        f"Ваши рефералы: {ref_count}\n"
        f"[Скопировать ссылку]({ref_link})"
    )
    
    # Placeholder for referral menu keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Поделиться ссылкой", url=ref_link)]
    ])
    
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
