# PASSIVE
# Refactored to aiogram 3.x - Step 4
# Removed duplicate functions - import from utils.py and ui_blocks.py instead

LANG = 'ru'
import sys, os, json, requests
import mimetypes
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram import Bot
from temporal import Adelay, Show_Game_Time, get_utc_string
from lifeman import save_timezone, get_role, get_pays, Get_DONNA_URL, Get_UNI_URL, Get_AXI0M_REF, Get_AXI5M_URL
from utils import Generate_Ref_Code, BOGDAN_URL, DONNA_URL, UNILIV_URL, AXIOM5_URL, AXIOM_REF, AXIOM_URL
# Import refactored functions from utils.py and ui_blocks.py (no longer duplicated here)
from utils import Get_Uid, Get_Var, Get_VAR, Set_Var, Update_step, UMR, ESC
from ui_blocks import SEX, SEFoB, SEFoM, Make_MENU, Make_MENB, Make_KEYB
from lifeBlock import LIFE_BLOCK

TARIFS = {
    5: {"vita": 50, "life": 2},
    10: {"vita": 100, "life": 5},
    20: {"vita": 200, "life": 11},
    50: {"vita": 500, "life": 25},
    100: {"vita": 1000, "life": 55},
    200: {"vita": 2000, "life": 125},
    500: {"vita": 5000, "life": 265},
    1000: {"vita": 10000, "life": 599}
}

# LIFE_BOOK = None
# LIFE_BLOCK = None
BOT_NAME = None
ART_DIR = None
ARTBLOK_DIR = None

class TEXTBLOCK:
    """
    Text block class for storing block data from LIFE_BLOCK dictionary.

    Attributes:
        id: Block ID
        title: Block title
        text: Block text content
        picture: Picture path
        menu: Menu buttons list
    """
    def __init__(self, item_id, title, text, picture, menu):
        self.id = item_id
        self.title = title
        self.text = text
        self.picture = picture
        self.menu = menu

    def display(self):
        print(f"ID: {self.id}")
        print(f"Title: {self.title}")
        print(f"Picture: {self.picture}")
        print(f"Menu: {self.menu}")
        print(f"Message: {self.text}")


def get_tariff_info(usdt_amount):
    """Get tariff info (index, vita, lifes) by USDT amount."""
    sorted_keys = sorted(TARIFS.keys())

    if usdt_amount not in TARIFS:
        return None, None, None  # Если такого тарифа нет

    index = sorted_keys.index(usdt_amount)
    vita = TARIFS[usdt_amount]["vita"]
    lifes = TARIFS[usdt_amount]["life"]

    return index, vita, lifes


def get_tariff_infoby_index(index):
    """Get tariff info (USDT, vita, life) by tariff index."""
    sorted_keys = sorted(TARIFS.keys())
    if 0 <= index < len(sorted_keys):
        usdt_key = sorted_keys[index]
        vita = TARIFS[usdt_key]["vita"]
        life = TARIFS[usdt_key]["life"]
        return usdt_key, vita, life  # Возвращаем USDT, Vita, Life
    else:
        return None, None, None  # Неверный индекс


def IsPREM():
    """Check if user has premium status."""
    return get_pays()

def IsUserPREM() -> bool:
    """Check if user is premium (pays > 0)."""
    prem = IsPREM()
    return prem>0

def IsUserPreme(role:str=None) -> bool:
    """Check if user is premium by role (contains '+')."""
    if role is None:
        role = get_role()
    return ('+' in role)


def Make_Block(block_name):
    """
    Create a block with text, keyboard, and picture from LIFE_BLOCK dictionary.

    Args:
        block_name: Block name or ID

    Returns:
        tuple: (block_text, keyboard, picture_path)
    """
    print("Make_Block > ", block_name)
    Block = Get_Block(block_name)
    # print(" > ", Block.title)
    if Block is None:
        return f"> Error find a block: {ESU(block_name)}", None, None
    # print("Text > ", Block.text.split('\n')[0])

    # Проверяем наличие картинки
    picture_path = None
    if Block.picture:
        picture_path = f"{Block.picture}.jpg"
        pic_file = os.path.join(ARTBLOK_DIR, picture_path)
        picture_path = pic_file if os.path.isfile(pic_file) else None
    print("Picture > ", picture_path)

    # Обрабатываем меню, если оно указано
    keyboard = None
    if Block.menu:
        buttons = []
        # Создаем кнопки из меню
        for button_data in Block.menu:
            callback = button_data["callback"]
            # Проверяем наличие "https" в callback
            if callback=="BOGDAN_URL":   callback = BOGDAN_URL
            elif callback=="DONNA_URL":   callback = DONNA_URL
            elif callback=="UNILIV_URL":   callback = UNILIV_URL
            elif callback=="AXIOM5_URL":   callback = AXIOM5_URL
            elif callback=="AXIOM0_URL":   callback = AXIOM_URL
            text=button_data["caption"]

            if "https" in callback:
                # Заменяем создание кнопки на создание с использованием url
                button = InlineKeyboardButton(
                    text=text,
                    url=callback  # Используем параметр url
                )
            else:
                button = InlineKeyboardButton(
                    text=text,
                    callback_data=callback
                )

            buttons.append([button])  # Каждый button в своей строке
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    print("Keyboard > ", str(keyboard).split('((')[-1])
    return Block.text, keyboard, picture_path


def REFRESHPART():
    """Refresh partner URLs from database."""
    global DONNA_URL, UNILIV_URL, AXIOM5_URL, AXIOM_REF
    try:
        if Get_DONNA_URL(): DONNA_URL = Get_DONNA_URL()
        if Get_UNI_URL(): UNILIV_URL = Get_UNI_URL()
        if Get_AXI5M_URL(): AXIOM5_URL = Get_AXI5M_URL()
        if Get_AXI0M_REF(): AXIOM_REF = Get_AXI0M_REF()
        # AXIOM_URL = Get_AXI0M_URL()
    except Exception as e: print(e)


def Get_Block(block_name):
    """
    Get block from LIFE_BLOCK dictionary by name or ID.

    Args:
        block_name: Block name (str) or ID (int)

    Returns:
        TEXTBLOCK object or None
    """
    # Проверяем, что LIFE_BLOCK существует и не пуст
    # print (LIFE_BLOCK)
    if not LIFE_BLOCK:
        return None

    REFRESHPART()
    # print('1ok')
    # Определяем тип block_name один раз
    if isinstance(block_name, str):        key = 'title'
    elif isinstance(block_name, int):      key = 'id'
    else:                               return None  # Возвращаем None, если тип block_name некорректный
    # print('2ok')
    # Ищем блок по ключу
    message = next((block for block in LIFE_BLOCK if block.get(key) == block_name), None)
    # print('3ok')
    # Если блок не найден, возвращаем None
    if message is None:         return None
    # print('4ok')
    # Создаем и возвращаем объект TEXTBLOCK
    return TEXTBLOCK(
        item_id=message.get('id'),
        title=message.get('title'),
        text=message.get('ru'),
        picture=message.get('picture'),
        menu=message.get('menu')
    )


def LOG_DIC_INITY(bot_name, art_dir, artblock_dir):
    """Initialize global variables for bot name and art directories."""
    global BOT_NAME, ART_DIR, ARTBLOK_DIR
    BOT_NAME = bot_name
    ART_DIR = art_dir
    ARTBLOK_DIR = artblock_dir
    return BOT_NAME

def del_update_flag(file_flag):
    """Delete update flag file."""
    print(f">DUF< {file_flag} задушен 👹")
    os.remove(file_flag)

def ESU(text):
    """
    Escape underscores in text for Telegram markdown.
    Adds extra underscore if count is odd.
    """
    text = str(text)
    count = text.count('_')
    if (count>0) and (count % 2 != 0): # нечет
        text+='_'
    # return text.replace('_', '')
    return text

def GetArt(pic:str):
    """Get art picture path (currently returns None)."""
    return None
    # print("GetArt> pic > ", pic)
    # art_pic = ArtBlock(pic)
    # print("GetArt> art_pic > ", art_pic)
    # pic_file = os.path.join(ART_DIR, art_pic)
    # print("GetArt> pic_file > ", pic_file)
    # ready = pic_file if os.path.isfile(pic_file) else None
    # return ready

def CYFER(message):
    """Convert digits in message to emoji digits."""
    number_icons = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣'   }
    beautiful_message = ''.join(number_icons.get(char, char) for char in message)
    return beautiful_message


def Create_user_folders(mod_dir, user_folder):
    """Create user directories for data storage."""
    path1 = mod_dir        # comon all users
    path2 = f'{path1}/{user_folder}'    # user
    os.makedirs(path1, exist_ok=True)
    os.makedirs(path2, exist_ok=True)
    return path1, path2

async def Update_utc_zone(offset, state):
    """
    Update user's UTC timezone string in state.

    Args:
        offset: Timezone offset
        state: FSMContext state object
    """
    utc_str = get_utc_string(offset)
    await Set_Var('user_utc', utc_str, state)

async def Update_User_ZONE(offset, state):
    """
    Update user's timezone in state.

    Args:
        offset: Timezone offset
        state: FSMContext state object
    """
    await Set_Var('user_tz', offset, state)
    # save_timezone(offset)
    # Update_step(19, state)
    await Update_utc_zone(offset, state)


def Comb_Reflink(code):
    """Combine bot name and referral code into referral link."""
    return f"{BOT_NAME}?start={code}"

async def Save_Refdata(Code, Link, state):
    """
    Save referral data to user state.

    Args:
        Code: Referral code
        Link: Referral link
        state: FSMContext state object
    """
    await Set_Var('user_refcode', Code, state)
    await Set_Var('user_reflink', Link, state)

async def Regen_Link(state):
    """
    Regenerate referral link for user.

    Args:
        state: FSMContext state object
    """
    # BOT_NAME = await Get_Var('BOT_NAME', state)
    Code  = Generate_Ref_Code()
    Link =  Comb_Reflink(Code)
    existing_link = await Get_Var('user_reflink', state)
    new = "новая " if existing_link else ""
    text = f"🤝 Ваша {new}партнерская ссылка успешно получена 👍🏻"
    print (text)
    print (Link)
    await Save_Refdata(Code, Link, state)


def Send_Stik(chat_id, sticker_id, token):
    """Send sticker via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{token}/sendSticker"
    DATA = {
        'chat_id': chat_id,
        'sticker': sticker_id}
    response = requests.post(url, params = DATA)
    return response.json()


async def Scroll_chat_down(bot: Bot, user_id: int):
    """
    Scroll chat down by sending invisible messages.

    Args:
        bot: aiogram Bot instance
        user_id: User ID to scroll chat for

    Returns:
        bool: False always
    """
    # Используем невидимый символ Unicode  # invisible_character = "\u200B"
    message = " "
    max_attempts = 2
    # Отправляем сообщение с эмодзи и сохраняем его
    last_message = await bot.send_message(chat_id=user_id, text="⌛️")

    print("@ Начали скроллинг.", end='', flush=True)
    for attempt in range(max_attempts):
        try:
            print(".>.", end='', flush=True)
            await bot.send_message(
                chat_id=user_id,
                text=message,
                disable_notification=True)
            print("Скроллинг выполнен успешно @", flush=True)
            break
        except Exception as e:
            if attempt < max_attempts - 1:
                print("_", end='', flush=True)
                await Adelay(2)  # Ждем 2 сек перед следующей попыткой
    print("Забили на скроллинг @", flush=True)
    # Удаляем сообщение с эмодзи
    try:
        await delete_bot_message(last_message, bot)
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")
    return False

async def delete_bot_message(message, bot: Bot):
    """
    Delete bot message by message object.

    Args:
        message: Message object to delete
        bot: aiogram Bot instance
    """
    if message and hasattr(message, 'chat') and hasattr(message, 'message_id'):
        try:
            chat_id = message.chat.id
            print(f"Пробуем удалить сообщение {message.message_id} в чате {chat_id}")
            await bot.delete_message(
                chat_id=chat_id,
                message_id=message.message_id
            )
            print("Сообщение успешно удалено")
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")
    else:
        print("Некорректный объект сообщения для удаления")


async def MAKE_DAYBACK(state):
    """Send day back button message."""
    await SEX("/start👉🏻Меню🕰Дня  /help👉🏻Помощь❓Команд", state)

async def MAKE_REFBACK(state):
    """Send referral back button message."""
    await SEX("🔰 Возврат в Реферальную Панель 👉🏻 /refer", state)

async def delete_user_message(message: Message, bot: Bot):
    """
    Delete user message.

    Args:
        message: Message object to delete
        bot: aiogram Bot instance
    """
    if message.from_user.id != bot.id:
        try: # Удаляем сообщение пользователя
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id)
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")


def load_dict(ant_dict):
    """Load dictionary from JSON file."""
    print(f">>> {ant_dict} > ", end='')
    try:
        with open(ant_dict, 'r', encoding='utf-8') as f:
            dictt = json.load(f)
        print("СЛОВАРЬ ЗАГРУЖЕН")
        return dictt
    except FileNotFoundError:
        print("СЛОВАРЬ НЕ НАЙДЕН!")
        return None
    except json.JSONDecodeError:
        print("СЛОВАРЬ СЛОМАЛСЯ! проверь JSON в конфиге!")
        return None

def load_config():
    """Load config from config.json file."""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print(">>> Конфиг загружен! ", end='')
        return config
    except FileNotFoundError:
        print(">>> Конфиг-файл не найден! Да и хрен с ним ")
        return None
    except json.JSONDecodeError:
        print(">>> Хреновый JSON в конфиге! Игнорируем его ")
        return None
