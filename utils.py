import os
import json
import html
import asyncio
from datetime import datetime, timedelta, time
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from babel.dates import format_date
import pytz
from tzlocal import get_localzone
import time as time_module
from time import sleep

# Global variables for configuration (will be set from config.json or similar)
BOT_NAME = None
ART_DIR = None
ARTBLOK_DIR = None

# User data management using aiogram 3.x FSMContext
async def Get_Uid(state: FSMContext):
    """Get user ID from FSM state storage."""
    data = await state.get_data()
    return data.get('user_id')

async def Get_Var(variable: str, state: FSMContext):
    """Get a variable from FSM state storage."""
    data = await state.get_data()
    return data.get(variable)

async def Get_VAR(variable: str, defvalue, state: FSMContext):
    """Get a variable from FSM state storage with default value."""
    data = await state.get_data()
    return data.get(variable, defvalue)

async def Set_Var(variable: str, value, state: FSMContext):
    """Set a variable in FSM state storage."""
    await state.update_data({variable: value})

async def Update_step(index, state: FSMContext):
    """Update the current step index in FSM state."""
    await Set_Var('step', index, state)

# File and directory utilities
def Create_user_folders(mod_dir, user_folder):
    path1 = mod_dir
    path2 = f'{path1}/{user_folder}'
    os.makedirs(path1, exist_ok=True)
    os.makedirs(path2, exist_ok=True)
    return path1, path2

def del_update_flag(file_flag):
    print(f">DUF< {file_flag} задушен 👹")
    os.remove(file_flag)

# Text formatting and escaping
def ESU(text):
    text = str(text)
    count = text.count('_')
    if (count > 0) and (count % 2 != 0): # нечет
        text += '_'
    return text

def ESC(text: str):
    return html.escape(text)

def CYFER(message):
    number_icons = {
        '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣',
        '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'
    }
    beautiful_message = ''.join(number_icons.get(char, char) for char in message)
    return beautiful_message

def pluralize_ru(number, one, few, many):
    if number % 10 == 1 and number % 100 != 11:
        return f"{number} {one}"
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return f"{number} {few}"
    else:
        return f"{number} {many}"

# Time and date utilities
SERVER_TIMEZONE = pytz.timezone('Europe/Moscow') # Default, will be updated by get_server_timezone
CLIENT_TIMEZONE = pytz.UTC
CLIENT_OFFSET = 0

def get_server_timezone():
    global SERVER_TIMEZONE
    SERVER_TIMEZONE = get_localzone()
    return SERVER_TIMEZONE

def get_utc_string(offset):
    global CLIENT_OFFSET
    CLIENT_OFFSET = offset
    try:
        offset_value = int(float(offset))
    except ValueError:
        return "get_utc_string > Invalid offset"
    return f"UTC{offset_value:+d}"

def get_server_time(zone = SERVER_TIMEZONE) -> datetime:
    return datetime.now(zone)

def get_custom_time(client_offset) -> datetime:
    if isinstance(client_offset, str):
        client_offset = int(client_offset)
    utc_now = get_server_time(pytz.UTC)
    offset = timedelta(hours=client_offset)
    client_time = utc_now + offset
    return client_time

def get_client_time() -> datetime:
    return get_custom_time(CLIENT_OFFSET)

def get_time():
    return get_server_time(), get_client_time()

def T2str(stime):
    if isinstance(stime, time):
        return stime.strftime('%H:%M')
    elif isinstance(stime, datetime):
        return stime.strftime('%H:%M')
    else:
        raise TypeError("T2str Аргумент должен быть объектом datetime или time")

def T2STR(stime):
    if isinstance(stime, time):
        return stime.strftime('%H:%M:%S')
    elif isinstance(stime, datetime):
        return stime.strftime('%H:%M:%S')
    else:
        raise TypeError("T2str Аргумент должен быть объектом datetime или time")

def S2TIME(time_string):
    time_string = time_string.strip()
    try:
        if ' ' in time_string:
            return datetime.fromisoformat(time_string)
        elif ':' in time_string:
            parts = time_string.split(':')
            if len(parts) != 2:
                raise ValueError("Неправильный формат времени. Ожидалось 'HH:MM'")
        elif '-' in time_string:
            parts = time_string.split('-')
            if len(parts) != 2:
                raise ValueError("Неправильный формат времени. Ожидалось 'HH-MM'")
        else:
            raise ValueError("Неправильный формат времени. Ожидалось 'HH:MM' или 'YYYY-MM-DD HH:MM'")
        hours = int(parts[0])
        minutes = int(parts[1])
        if not (0 <= hours < 24) or not (0 <= minutes < 60):
            raise ValueError("Часы должны быть в диапазоне 0-23, минуты - в диапазоне 0-59.")
        now = get_server_time()
        return datetime(now.year, now.month, now.day, hours, minutes)
    except ValueError as e:
        raise ValueError(f"Ошибка: {e}")
    except Exception as e:
        raise Exception(f"Неизвестная ошибка: {e}")

def Shot(atime):
    return atime.replace(microsecond=0) if isinstance(atime, datetime) else atime

def shot(atime):
    if isinstance(atime, datetime):
       atime = T2STR(atime)
    if '.' in atime:
        return atime.split('.')[0]
    else:
        return atime

def get_month_name(date):
    return format_date(date, format='MMMM', locale='ru')

def format_time_ru(hours, minutes):
    hours_str = pluralize_ru(hours, "час", "часа", "часов")
    minutes_str = pluralize_ru(minutes, "минута", "минуты", "минут")
    return f"{hours_str} {minutes_str}"

def format_times_ru(hours, minutes, seconds):
    hours_str = pluralize_ru(hours, "час", "часа", "часов")
    minutes_str = pluralize_ru(minutes, "минута", "минуты", "минут")
    seconds_str = pluralize_ru(seconds, 'секунда', 'секунды', 'секунд')
    return f"{hours_str} {minutes_str} {seconds_str}"

async def Adelay(delay):
    await asyncio.sleep(delay)

def Sdelay(delay):
    sleep(delay)

def localize_time(ZONE, native_datetime):
    if isinstance(native_datetime, str):
        native_datetime = S2TIME(native_datetime)
    if not isinstance(native_datetime, datetime):
        raise TypeError("native_datetime должен быть строкой или объектом datetime")
    return native_datetime.replace(tzinfo=ZONE)

def Show_Time_Info(time_obj):
    if isinstance(time_obj, timedelta):
        total_seconds = int(time_obj.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
    elif isinstance(time_obj, datetime):
        hours = time_obj.hour
        minutes = time_obj.minute
        seconds = time_obj.second
    else:
        raise TypeError("Ожидается объект datetime или timedelta")
    stime = format_time_ru(hours, minutes)
    ftime = format_times_ru(hours, minutes, seconds)
    print("Форматируем Время под Русский > ", ftime)
    return stime

def Show_Game_Time(user_stime):
    shorts = Shot(user_stime)
    print(f"ShowGameTime > Игра стартовала: {shorts}")
    user_stime = S2TIME(user_stime) if isinstance(user_stime, str) else user_stime
    now = get_server_time()
    elapsed_time = get_delta(user_stime, now)
    stime = Show_Time_Info(elapsed_time)
    print(f"ShowGameTime > Время в игре: {stime}")
    return stime

def get_delta(first_date: datetime, second_date: datetime) -> timedelta:
    localized_first_date = first_date if first_date.tzinfo else SERVER_TIMEZONE.localize(first_date)
    localized_second_date = second_date if second_date.tzinfo else CLIENT_TIMEZONE.localize(second_date)
    delta = localized_second_date - localized_first_date
    return delta

def days_passed(target_date: datetime) -> int:
    now = get_server_time()
    delta = get_delta(target_date, now)
    return delta.days

# Configuration loading
def load_dict(ant_dict):
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

# Placeholder for Generate_Ref_Code (will be in referral_logic.py)
def Generate_Ref_Code():
    # This should be implemented in referral_logic.py
    return "REFCODE123"
