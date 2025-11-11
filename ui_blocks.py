import os
import mimetypes
import html
from logger import logger
from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
import requests  # For Send_Stik
from typing import Any, Dict, List, Optional, Union, Callable, Awaitable
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, 
    ReplyKeyboardMarkup, KeyboardButton, 
    Message, ReplyKeyboardRemove, CallbackQuery
)
from lifeBlock import LIFE_BLOCK  # For Send_Stik
from utils import Get_Uid, Get_Var, Adelay, ESC, ESU
from const import (
    ARTBLOK_DIR,
    BOGDAN_URL, 
    DONNA_URL, 
    UNILIV_URL, 
    AXIOM5_URL, 
    AXIOM_REF, 
    AXIOM_URL,
    REFRESHPART
)
from art_utils import get_art as GetArt  # Import from our new utility module
from typing import Optional, Dict, Any, List
import json
import os
from typing import Optional, Dict, Any, List
import json
import os

# Global variables for configuration (will be set from config.json or similar)
BOT_NAME = None  # Will be set from config

# Load life blocks
LIFE_BLOCKS = {}

try:
    from lifeBlock import LIFE_BLOCK as LIFE_BLOCKS_LIST
    # Convert list to dict for faster lookup by title
    LIFE_BLOCKS = {block['title']: block for block in LIFE_BLOCKS_LIST if 'title' in block}
except ImportError:
    print("Warning: Could not import LIFE_BLOCK from lifeBlock.py")

def get_life_block(title: str) -> Optional[Dict[str, Any]]:
    """Retrieve a life block by title."""
    return LIFE_BLOCKS.get(title)

def get_life_block_titles() -> List[str]:
    """Retrieve a list of life block titles."""
    return list(LIFE_BLOCKS.keys())

def get_life_block_count() -> int:
    """Retrieve the number of life blocks."""
    return len(LIFE_BLOCKS)

# Parse mode constants
PARSE_MODE_HTML = 'HTML'
PARSE_MODE_MARKDOWN = 'Markdown'  # Using Markdown v1

async def SEX(
    text: str, 
    context: ContextTypes.DEFAULT_TYPE, 
    SENDER: int = None, 
    DOC = None, 
    EDIT = None, 
    MENU = None, 
    FORMAT: str = None
):
    """
    Universal function for sending and editing messages with aiogram 3.x
    
    Args:
        text: Message text
        context: Context object
        SENDER: Optional chat_id to send to
        DOC: Document to send (path or InputFile)
        EDIT: Message ID to edit (if editing)
        MENU: Inline keyboard markup
        FORMAT: Format string (e.g., 'HTML', 'Markdown')
        
    Returns:
        Message object or None if error
    """
    from aiogram.types import Message, InputFile as AiogramInputFile
    from aiogram.enums import ParseMode
    
    try:
        # Get user and chat IDs
        user_id = context.user.id if hasattr(context, 'user') else None
        chat_id = SENDER if SENDER else (context.chat.id if hasattr(context, 'chat') else user_id)
        
        if not chat_id:
            raise ValueError("No chat_id available for sending message")
            
        # Parse format options
        parse_mode = None
        if FORMAT:
            if 'H' in FORMAT:
                parse_mode = ParseMode.HTML
                text = ESC(text) if text else text
            elif 'B' in FORMAT:
                parse_mode = 'Markdown'
        
        # Handle message editing
        if EDIT:
            if DOC:
                # Edit message with document
                return await context.bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=EDIT,
                    caption=text,
                    reply_markup=MENU,
                    parse_mode=parse_mode
                )
            elif text is None and MENU is not None:
                # Edit only reply markup
                return await context.bot.edit_message_reply_markup(
                    chat_id=chat_id,
                    message_id=EDIT,
                    reply_markup=MENU
                )
            else:
                # Edit text message
                return await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=EDIT,
                    text=text,
                    reply_markup=MENU,
                    parse_mode=parse_mode,
                    disable_web_page_preview=True
                )
                
        # Handle document sending
        if DOC:
            if not isinstance(DOC, AiogramInputFile):
                DOC = AiogramInputFile(DOC)
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(DOC.filename)
            
            # Handle different document types
            if mime_type == 'audio/ogg':
                return await context.bot.send_voice(
                    chat_id=chat_id,
                    voice=DOC,
                    caption=text,
                    reply_markup=MENU,
                    parse_mode=parse_mode
                )
            elif mime_type and mime_type.startswith('image/'):
                return await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=DOC,
                    caption=text,
                    reply_markup=MENU,
                    parse_mode=parse_mode
                )
            elif mime_type and mime_type.startswith('video/'):
                return await context.bot.send_video(
                    chat_id=chat_id,
                    video=DOC,
                    caption=text,
                    reply_markup=MENU,
                    parse_mode=parse_mode
                )
            else:
                # Default to document
                return await context.bot.send_document(
                    chat_id=chat_id,
                    document=DOC,
                    caption=text,
                    reply_markup=MENU,
                    parse_mode=parse_mode
                )
        
        # Default text message
        return await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=MENU,
            parse_mode=parse_mode,
            disable_web_page_preview=True
        )

    except Exception as e:
        logger.error(f"Error in SEX function: {e}", exc_info=True)
        return None

async def SEFoB(block, block_tex:str, context: ContextTypes.DEFAULT_TYPE):
    block_pic = GetArt(block)
    if block_pic:
        print ("SEFoB: Найдена фотка, отправляем фото-блок")
        with open(block_pic, 'rb') as photo:
            await SEX(block_tex, context, DOC = photo, FORMAT = 'B')
    else:
        print ("SEFoB: Фотка не найдена, отправляем текст")
        await SEX(block_tex, context, FORMAT = 'B')

async def SEFoM(block, block_tex, keyb, context: ContextTypes.DEFAULT_TYPE):
    block_pic = GetArt(block)
    if block_pic:
        print ("SEFoM: Найдена фотка, отправляем фото-блок c меню")
        with open(block_pic, 'rb') as photo:
            await SEX(block_tex, context, DOC = photo, MENU = keyb, FORMAT = 'B')
    else:
        print ("SEFoM: Фотка не найдена, отправляем текст c меню")
        await SEX(block_tex, context, MENU = keyb, FORMAT = 'B')

async def Make_MENU(text, buttons, context: ContextTypes.DEFAULT_TYPE):
    keyboard = Make_KEYB(buttons)
    return await SEX(text, context, MENU=keyboard)

async def Make_MENB(text, buttons, context: ContextTypes.DEFAULT_TYPE):
    keyboard = Make_KEYB(buttons)
    return await SEX(text, context, MENU=keyboard, FORMAT = 'B')

def Make_KEYB(buts):
    return InlineKeyboardMarkup(buts)

def Send_Stik(chat_id, sticker_id, token):
    url = f"https://api.telegram.org/bot{token}/sendSticker"
    DATA = {
        'chat_id': chat_id,
        'sticker': sticker_id}
    response = requests.post(url, params = DATA)
    return response.json()

async def Scroll_chat_down(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = Get_Uid(context)
    message = " "
    max_attempts = 2
    last_message = await context.bot.send_message(chat_id=user_id, text="⌛️")
    print("@ Начали скроллинг.", end='', flush=True)
    for attempt in range(max_attempts):
        try:
            print(".>.", end='', flush=True)
            await context.bot.send_message(
                chat_id=user_id,
                text=message,
                disable_notification=True)
            print("Скроллинг выполнен успешно @", flush=True)
            break
        except Exception as e:
            if attempt < max_attempts - 1:
                print("_", end='', flush=True)
                await Adelay(2)
    print("Забили на скроллинг @", flush=True)
    try:
        await delete_bot_message(last_message, context)
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")
    return False

async def delete_bot_message(message, context: ContextTypes.DEFAULT_TYPE):
    if message and hasattr(message, 'chat_id') and hasattr(message, 'message_id'):
        try:
            print(f"Пробуем удалить сообщение {message.message_id} в чате {message.chat_id}")
            await context.bot.delete_message(
                chat_id=message.chat_id,
                message_id=message.message_id
            )
            print("Сообщение успешно удалено")
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")
    else:
        print("Некорректный объект сообщения для удаления")

async def UMR(text:str, update: Update):
    return await update.message.reply_text(text)

async def MAKE_DAYBACK(context: ContextTypes.DEFAULT_TYPE):
    await SEX("/start👉🏻Меню🕰Дня  /help👉🏻Помощь❓Команд", context)

async def MAKE_REFBACK(context: ContextTypes.DEFAULT_TYPE):
    await SEX("🔰 Возврат в Реферальную Панель 👉🏻 /refer", context)

async def delete_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last_message = update.effective_message
    if last_message.from_user.id != context.bot.id:
        try:
            await context.bot.delete_message(
                chat_id=last_message.chat_id,
                message_id=last_message.message_id
            )
        except Exception as e:
            print(f"Error deleting message: {e}")

def get_block(block_name: str) -> Optional[Dict[str, Any]]:
    """
    Get a block by its name from LIFE_BLOCK with flexible matching.
    
    Args:
        block_name: The name of the block to retrieve (can be title, B_ prefix, or ID)
        
    Returns:
        The block dictionary if found, None otherwise
    """
    if not block_name:
        return None
        
    # Remove B_ prefix if present for matching
    clean_name = block_name[2:] if block_name.startswith('B_') else block_name
    
    # Try exact title match first
    for block in LIFE_BLOCK:
        if block.get('title') == clean_name or block.get('title') == block_name:
            return block
    
    # Try case-insensitive match
    for block in LIFE_BLOCK:
        if block.get('title', '').lower() == clean_name.lower():
            return block
    
    # Try to find by ID if block_name is numeric
    if clean_name.isdigit():
        block_id = int(clean_name)
        for block in LIFE_BLOCK:
            if block.get('id') == block_id:
                return block
    
    # Try to find by partial match in title
    for block in LIFE_BLOCK:
        if clean_name in block.get('title', ''):
            return block
            
    return None
            
def format_block_text(block: Dict[str, Any], **kwargs) -> str:
    """Format block text with the given variables."""
    if not block:
        return ""
        
    text = block.get('ru', '')
    if not text:
        return ""
        
    try:
        return text.format(**kwargs)
    except (KeyError, ValueError):
        return text

def create_menu_from_block(block: Dict[str, Any]) -> Optional[InlineKeyboardMarkup]:
    """Create an inline keyboard from a block's menu definition."""
    try:
        if not block or 'menu' not in block or not block['menu']:
            return None
            
        keyboard = []
        for item in block['menu']:
            if not item or 'caption' not in item or 'callback' not in item:
                continue
                
            button = InlineKeyboardButton(
                text=str(item['caption']).strip(),
                callback_data=str(item['callback']).strip()
            )
            keyboard.append([button])
        
        if not keyboard:
            return None
            
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
        
    except Exception as e:
        print(f"Error creating menu: {str(e)}")
        return None


async def show_block(message, block_name: str, user_data: dict = None, final_callback=None, start_callback=None):
    """
    Show a specific block with proper formatting, including images and keyboards.
    
    Args:
        message: The message object to reply to
        block_name: Name of the block to show (e.g., 'JOIN1', 'START1')
        user_data: User data for text formatting
        final_callback: Callback for FINAL block
        start_callback: Callback for START block
    """
    from aiogram.types import InputFile
    from pathlib import Path
    
    # Get the block from lifeBlock.py
    block = get_block(block_name)
    if not block:
        await message.answer("❌ Ошибка: блок не найден")
        return

    def escape_markdown(text: str) -> str:
        if not isinstance(text, str):
            return str(text)
        # Escape all markdown v1 special characters
        special_chars = ['_', '*', '`', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        return text

    # Format text with user data if provided
    text = block.get('ru', '')
    if user_data:
        if hasattr(user_data, 'model_dump'):
            user_data = user_data.model_dump()
        if user_data:
            # First, handle the case where user_data is not a dictionary
            if not isinstance(user_data, dict):
                user_data = {}
            
            # Create a safe copy of user_data with escaped values
            safe_user_data = {k: escape_markdown(v) for k, v in user_data.items()}
            
            # Format the text with the safe data
            try:
                text = text.format(**safe_user_data)
            except (KeyError, ValueError):
                # If there are still formatting errors, try to handle them gracefully
                try:
                    from string import Formatter
                    formatter = Formatter()
                    result = []
                    for literal_text, field_name, format_spec, conversion in formatter.parse(text):
                        result.append(literal_text or '')
                        if field_name is not None:
                            try:
                                value = safe_user_data.get(field_name, f'{{{field_name}}}')
                                result.append(str(value))
                            except (KeyError, ValueError):
                                result.append(f'{{{field_name}}}')
                    text = ''.join(result)
                except Exception:
                    # If all else fails, use the original text
                    pass
    
    # Create keyboard if menu exists
    keyboard = create_menu_from_block(block)
    
    # First, escape the text to prevent markdown parsing errors
    try:
        # Escape markdown in the text
        text = escape_markdown(text)
    except Exception as e:
        print(f"Error escaping markdown: {str(e)}")
        # If escaping fails, try to send as plain text
        parse_mode = None
    else:
        parse_mode = 'Markdown'
        
    # Handle image if present
    picture = block.get('picture')
    if picture:
        try:
            # Get the bot's root directory (where this script is located)
            bot_root = Path(__file__).parent
            # Define relative path to images from bot root
            base_dir = bot_root / 'DATA-LIFE' / 'art-block'
            
            # Try to find the image file in the relative directory with different extensions
            image_path = None
            for ext in ['.jpg', '.png', '.jpeg', '.webp']:
                test_path = base_dir / f"{picture}{ext}"
                if test_path.exists():
                    image_path = test_path
                    logger.info(f"Found image at: {image_path}")
                    break
            
            if image_path and image_path.exists():
                try:
                    photo = InputFile(image_path)
                    if keyboard:
                        sent_message = await message.answer_photo(
                            photo=photo,
                            caption=text,
                            reply_markup=keyboard,
                            parse_mode='Markdown'
                        )
                    else:
                        sent_message = await message.answer_photo(
                            photo=photo,
                            caption=text,
                            parse_mode='Markdown'
                        )
                    return  # Exit after successfully sending the photo
                except Exception as photo_error:
                    logger.error(f"Error sending photo {image_path}: {str(photo_error)}")
                    # Fall through to text message if photo fails
            
            # If we get here, either the image wasn't found or there was an error sending it
            error_msg = f"⚠️ Изображение {picture} не найдено"
            logger.warning(error_msg)
            await message.answer(error_msg)
            sent_message = False
            
        except Exception as e:
            error_msg = f"Ошибка при обработке изображения {picture}: {str(e)}"
            logger.error(error_msg)
            await message.answer(error_msg)
            sent_message = False
    else:
        sent_message = False
    
    # If no image was sent or there was an error, send text message
    if not sent_message:
        try:
            if keyboard:
                await message.answer(
                    text=text,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
            else:
                await message.answer(
                    text=text,
                    parse_mode='Markdown'
                )
        except Exception as e:
            # If markdown parsing fails, try sending as plain text
            print(f"Markdown error: {e}")
            try:
                if keyboard:
                    await message.answer(
                        text=text,
                        reply_markup=keyboard,
                        parse_mode=None
                    )
                else:
                    await message.answer(
                        text=text,
                        parse_mode=None
                    )
            except Exception as e:
                print(f"Error sending message: {e}")
                # If all else fails, send a simple error message
                await message.answer("Произошла ошибка при отображении блока.")
    
    # Special handling for certain blocks
    if block_name == 'FINAL' and final_callback:
        await final_callback(message, user_data or {})
    elif block_name.startswith('START') and start_callback:
        await start_callback(block_name, message, user_data or {})

async def send_block(
    block_title: str, 
    context: ContextTypes.DEFAULT_TYPE, 
    chat_id: int = None, 
    **format_kwargs
) -> bool:
    """Send a block by its title."""
    block = get_block(block_title)
    if not block:
        print(f"Block '{block_title}' not found")
        return False
        
    text = format_block_text(block, **format_kwargs)
    keyboard = create_menu_from_block(block)
    picture = block.get('picture')
    
    if not chat_id:
        if hasattr(context, 'chat') and hasattr(context.chat, 'id'):
            chat_id = context.chat.id
        elif hasattr(context, 'user') and hasattr(context.user, 'id'):
            chat_id = context.user.id
        else:
            print("No chat_id available")
            return False
    
    try:
        if picture:
            picture_path = GetArt(picture)
            if picture_path and os.path.exists(picture_path):
                with open(picture_path, 'rb') as photo:
                    await SEX(
                        text=text,
                        context=context,
                        SENDER=chat_id,
                        DOC=photo,
                        MENU=keyboard,
                        FORMAT='B'  # MarkdownV2
                    )
            else:
                await SEX(
                    text=text,
                    context=context,
                    SENDER=chat_id,
                    MENU=keyboard,
                    FORMAT='B'  # MarkdownV2
                )
        else:
            await SEX(
                text=text,
                context=context,
                SENDER=chat_id,
                MENU=keyboard,
                FORMAT='B'  # MarkdownV2
            )
        return True
    except Exception as e:
        print(f"Error sending block {block_title}: {e}")
        return False

# Alias for backward compatibility
SEX_PRO = send_block

async def SEX_PROD(block_pak, context: ContextTypes.DEFAULT_TYPE):
    """Display a product block with the specified name."""
    return await send_block(block_pak, context)

def SEMOD(message, keyboard, context: ContextTypes.DEFAULT_TYPE, SENDER_ID: int):
    """Send a message with the specified keyboard to the specified user."""
    return SEX(message, context, SENDER=SENDER_ID, MENU=keyboard)


def build_main_menu(user_data: dict = None) -> InlineKeyboardMarkup:
    """Build the main menu keyboard.
    
    Args:
        user_data: Dictionary containing user data (optional)
        
    Returns:
        InlineKeyboardMarkup: The main menu keyboard
    """
    buttons = [
        [InlineKeyboardButton(text="📅 Дневник", callback_data="daily")],
        [InlineKeyboardButton(text="📊 Прогресс", callback_data="progress")],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_profile_menu(user_data: dict) -> InlineKeyboardMarkup:
    """Build the profile menu keyboard.
    
    Args:
        user_data: Dictionary containing user data
        
    Returns:
        InlineKeyboardMarkup: The profile menu keyboard
    """
    buttons = [
        [InlineKeyboardButton(text="✏️ Изменить ник", callback_data="change_nickname")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_settings_menu(user_data: dict) -> InlineKeyboardMarkup:
    """Build the settings menu keyboard.
    
    Args:
        user_data: Dictionary containing user data
        
    Returns:
        InlineKeyboardMarkup: The settings menu keyboard
    """
    # Get current notification settings from user_data
    notify_morning = user_data.get('notify_morning', True)
    notify_evening = user_data.get('notify_evening', True)
    
    buttons = [
        [
            InlineKeyboardButton(
                text=f"🌅 Утренние уведомления: {'✅' if notify_morning else '❌'}",
                callback_data="toggle_morning"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"🌆 Вечерние уведомления: {'✅' if notify_evening else '❌'}",
                callback_data="toggle_evening"
            )
        ],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_help_menu() -> InlineKeyboardMarkup:
    """Build the help menu keyboard.
    
    Returns:
        InlineKeyboardMarkup: The help menu keyboard
    """
    buttons = [
        [InlineKeyboardButton(text="📚 Команды бота", callback_data="bot_commands")],
        [InlineKeyboardButton(text="ℹ️ О марафоне", callback_data="about_marathon")],
        [InlineKeyboardButton(text="📞 Поддержка", url="https://t.me/your_support")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_marathon_progress(user_data: dict) -> InlineKeyboardMarkup:
    """Build the marathon progress menu keyboard.
    
    Args:
        user_data: Dictionary containing user data
        
    Returns:
        InlineKeyboardMarkup: The progress menu keyboard
    """
    current_day = user_data.get('current_day', 1)
    total_days = user_data.get('total_days', 28)  # Assuming 28-day marathon
    
    buttons = [
        [InlineKeyboardButton(text=f"📆 День {current_day} из {total_days}", callback_data="current_day")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="🏆 Достижения", callback_data="achievements")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
