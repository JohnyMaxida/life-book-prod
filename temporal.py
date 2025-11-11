# TEMPORAL
"""
Temporal functions for time and timezone management.
Pure Python module - no Telegram API dependencies.
"""
# Removed unused import: from telegram import Update
import asyncio, pytz, requests
from tzlocal import get_localzone
from datetime import time, datetime, timedelta, timezone, tzinfo
import time as time_module
from time import sleep  # Импортируем только sleep
from babel.dates import format_date
# pytz.timezone('Asia/Bangkok')
# from timezonefinder import TimezoneFinder
icons = ["🕥", "🕒", "🕗", "🧭", "⏰", "🕰", "⏳", "♻️",  "🐹", "🌏", "👀", "⌛"]
chrono_clock = "🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛🕜🕝🕞🕟🕠🕡🕢🕣🕤🕥🕦🕧"
SERVER_TIMEZONE = pytz.timezone('Europe/Moscow') 
CLIENT_TIMEZONE = pytz.UTC
CLIENT_OFFSET = 0
# shorts = user_stime.split('.')[0]  # удаляем миллисекунды + зону
# shorts = Shot(user_stime)  # удаляем миллисекунды   


def Is_date_sunday(dat:datetime):
    return dat.weekday() == 6

def Is_day_sunday(day:int, start_date:datetime):
    new_date = start_date + timedelta(days=day)        
    return Is_date_sunday(new_date)   

def get_delta(first_date: datetime, second_date: datetime) -> int:   
    print(f">DELTA>DATE1> {first_date}")
    # Убедитесь, что first_date локализован
    localized_first_date = first_date if first_date.tzinfo else SERVER_TIMEZONE.localize(first_date)
    # print(f">DELTA>DATE1>LOC> {localized_first_date}") 
    short_first_date = Shot(localized_first_date) 
    # print(f">DELTA>DATE1>LOC>SHOT {short_first_date}")    
    print(f">DELTA>DATE2> {second_date}")    
    # Убедитесь, что second_date локализован
    localized_second_date = second_date if second_date.tzinfo else CLIENT_TIMEZONE.localize(second_date)
    # print(f">DELTA>DATE2>LOC> {localized_second_date}") 
    short_second_date = Shot(second_date) 
    # print(f">DELTA>DATE2>LOC>SHOT> {short_second_date}")
    delta = localized_second_date - localized_first_date
    # delta = short_second_date - short_first_date    
    print(f">DELTA>=>shift<=> {delta}") 
    return delta

    
def days_until(target_date: datetime) -> int:
    now = get_server_time()
    # Убедитесь, что now локализован
    localized_now = now if now.tzinfo else SERVER_TIMEZONE.localize(now)    
    delta = get_delta(localized_now, target_date)
    return delta.days    

def days_passed(target_date: datetime) -> int:
    now = get_server_time()
    delta = get_delta(target_date, now)
    return delta.days 

def get_target_date(year, month, day):
    return datetime(year, month, day)
    
def Show_Game_Time(user_stime):
    # shorts = user_stime.split('.')[0]  # удаляем миллисекунды + зону
    shorts = Shot(user_stime)  # удаляем миллисекунды     
    print(f"ShowGameTime > Игра стартовала: {shorts}")
    user_stime = S2TIME(user_stime) if isinstance(user_stime, str) else user_stime
    now = get_server_time()        
    elapsed_time = get_delta(user_stime, now)
    stime = Show_Time_Info(elapsed_time)    
    print(f"ShowGameTime > Время в игре: {stime}")
    return stime

def get_server_timezone():
    global SERVER_TIMEZONE
    SERVER_TIMEZONE = get_localzone()
    return SERVER_TIMEZONE  

def get_utc_string(offset):
    global CLIENT_OFFSET
    CLIENT_OFFSET = offset
    try:
        offset_value = int(float(offset))  # Преобразуем строку в float, затем в int
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
# Удаляем пробелы в начале и в конце строки
    time_string = time_string.strip()    
# Проверка на формат "YYYY-MM-DD HH:MM" или "HH:MM"
    try:
        if ' ' in time_string:  # Если время в формате "YYYY-MM-DD HH:MM"
            return datetime.fromisoformat(time_string)
        elif ':' in time_string:  # Если время в формате "HH:MM"
            # Разделяем часы и минуты
            parts = time_string.split(':')
            if len(parts) != 2:
                raise ValueError("Неправильный формат времени. Ожидалось 'HH:MM'")
        elif '-' in time_string:  # Если время в формате "HH:MM"
            # Разделяем часы и минуты
            parts = time_string.split('-')
            if len(parts) != 2:
                raise ValueError("Неправильный формат времени. Ожидалось 'HH-MM'")
        else:
            raise ValueError("Неправильный формат времени. Ожидалось 'HH:MM' или 'YYYY-MM-DD HH:MM'")
# Преобразуем часы и минуты в целые числа
        hours = int(parts[0])
        minutes = int(parts[1])
# Проверяем на корректность значений
        if not (0 <= hours < 24) or not (0 <= minutes < 60):
            raise ValueError("Часы должны быть в диапазоне 0-23, минуты - в диапазоне 0-59.")
        # Получаем текущее время для установки даты
        now = get_server_time()
        return datetime(now.year, now.month, now.day, hours, minutes)
    except ValueError as e:
        raise ValueError(f"Ошибка: {e}")
    except Exception as e:
        raise Exception(f"Неизвестная ошибка: {e}")

def Shot(atime): # удаляем миллисекунды
    return atime.replace(microsecond=0) if isinstance(atime, datetime) else atime  

def shot(atime): # удаляем миллисекунды+зону 
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

def pluralize_ru(number, one, few, many):
    if number % 10 == 1 and number % 100 != 11:
        return f"{number} {one}"
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return f"{number} {few}"
    else:
        return f"{number} {many}"

async def Adelay(delay):
    await asyncio.sleep(delay)
    
def Sdelay(delay):
    sleep(delay)     
    
def localize_time(ZONE, native_datetime):
    if isinstance(native_datetime, str):
        # Предполагаем, что строка в формате "YYYY-MM-DD HH:MM:SS"
        native_datetime = S2TIME(native_datetime) # datetime.strptime(native_datetime, "%Y-%m-%d %H:%M:%S")    
    if not isinstance(native_datetime, datetime):
        raise TypeError("native_datetime должен быть строкой или объектом datetime")
    return native_datetime.replace(tzinfo=ZONE)  

def Show_Time_Info(time_obj):
    if isinstance(time_obj, timedelta):
# Если это timedelta, преобразуем его в часы, минуты и секунды
        total_seconds = int(time_obj.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
    elif isinstance(time_obj, datetime):
# Если это datetime, используем его напрямую
        hours = time_obj.hour
        minutes = time_obj.minute
        seconds = time_obj.second
    else:
        raise TypeError("Ожидается объект datetime или timedelta")
    stime = format_time_ru(hours, minutes)
    ftime = format_times_ru(hours, minutes, seconds)
    print("Форматируем Время под Русский > ", ftime)
    return stime 
    
# =========================-==========================-=========================

    # {'status': 'success', 'country': 'Thailand', 'countryCode': 'TH', 'region': '41', 'regionName': 'Udon Thani', 'city': 'Udon Thani', 'zip': '41000', 'lat': 17.135, 'lon': 102.972, 'timezone': 'Asia/Bangkok', 'isp': 'Triple T Broadband Public Company Limited', 'org': 'Triple T Broadband Public Company Limited', 'as': 'AS45758 Triple T Broadband Public Company Limited', 'query': '223.206.231.243'}

# =========================-==========================-=========================

# def get_client_offset(zone):
    # global CLIENT_TIMEZONE, CLIENT_OFFSET
    # timezone = pytz.UTC  # Изменяем на экземпляр UTC по умолчанию
    # if isinstance(zone, tzinfo):
        # timezone = zone
    # elif isinstance(zone, str):
        # timezone = pytz.timezone(zone)
    # else:
        # print('get_client_offset ошибка типа timezone')
        # return None  # Возвращаем None в случае ошибки
# Запоминаем используемую временную зону и смещение
    # CLIENT_TIMEZONE = timezone
    # client_time = get_client_time()
    # CLIENT_OFFSET = timezone.utcoffset(client_time).total_seconds() / 3600
    # return CLIENT_OFFSET


# def get_client_time() -> datetime:
    # print(f"отладка CLIENT_TIMEZONE: {CLIENT_TIMEZONE}")
    # return datetime.now(CLIENT_TIMEZONE)

# def get_client_zone(offset):
    # global CLIENT_TIMEZONE, CLIENT_OFFSET
    # if isinstance(offset, str):
        # offset = int(offset)
    # CLIENT_OFFSET = offset
    # if offset==0:
        # CLIENT_TIMEZONE = pytz.UTC
        # return CLIENT_TIMEZONE
    # for tz in pytz.all_timezones:
        # timezone = pytz.timezone(tz)
        # if timezone.utcoffset(datetime.now()) == timedelta(hours=offset):
            # CLIENT_TIMEZONE = timezone
            # break    
    # return CLIENT_TIMEZONE

    # life_request = "https://ipinfo.io"     # f"https://ipinfo.io/{ip}?token=44b7b7241f4605", 
    # response = requests.get(life_request)
    # data = response.json()
    # print (data)
    # STATUS = data['country']+", "+data['region']
    # TZ_STR = data['timezone']    
    # timezone = pytz.timezone(TZ_STR)

# def get_client_ip():
    # try:
        # response = requests.get('https://api.ipify.org?format=json')
        # data = response.json()
        # print(f"Получен IP-юзера: {data['ip']}")
        # return data['ip']
    # except Exception as e:
        # print(f"Ошибка при получении IP-адреса: {e}")
        # return None

# def get_timezone_from_ip(ip):
    # try:
        # response = requests.get(f'http://ip-api.com/json/{ip}')
        # data = response.json()
        # if data['status'] == 'success':            
            # print(data)            
            # return data['timezone'], data
        # else:
            # print(f"Ошибка get_timezone_from_ip: {data['message']}")
            # return None
    # except Exception as e:
        # print(f"Ошибка get_timezone_from_ip получении временной зоны: {e}")
        # return None
  
# def get_safe_timezone(tz_str):
    # try:
        # return pytz.timezone(tz_str)
    # except pytz.exceptions.UnknownTimeZoneError:
        # print(f"Неизвестная временная зона: {tz_str}. Используется UTC.")
        # return pytz.UTC  


# def get_client_zone() -> int:
    # global CLIENT_TIMEZONE, CLIENT_OFFSET 
    # TZ_STR, STATUS = "utc", "не получен"
    # ip = get_client_ip()
    # if ip:
        # STATUS = f"IP: {ip}" 
        # TZ_STR, U_DATA = get_timezone_from_ip(ip)        
        # if U_DATA:
            # STATUS += f" {U_DATA['country']}"        
    # timezone = get_safe_timezone(TZ_STR)
    # CLIENT_TIMEZONE = timezone   
    # client_time = get_client_time()
    # offset_seconds = client_time.utcoffset().total_seconds()
    # CLIENT_OFFSET = int(offset_seconds / 3600)
    # return CLIENT_TIMEZONE, CLIENT_OFFSET, STATUS, U_DATA

# def get_client_zone() -> int:
    # global CLIENT_OFFSET, CLIENT_TIMEZONE
    # timezone = datetime.now().astimezone().tzinfo
    # CLIENT_TIMEZONE = timezone
# Получение информации о местоположении пользователя через API
            # ip = "user_ip_address"  # Здесь нужно как-то получить IP пользователя
            # response = requests.get(f"http://ip-api.com/json/{ip}")
            # if data['status'] == 'success':
                # timezone = data['timezone']
    
    # response = requests.get('https://ipinfo.io')
    # data = response.json()
    # tz_client = data['timezone']
# Создаем объект timezone из строки tz_client
    # timezone = pytz.timezone(tz_client)
    # CLIENT_TIMEZONE = timezone    
# Получаем текущее время в этом часовом поясе
    # client_time = datetime.now(timezone)    
# Получаем смещение в секундах и переводим в часы
    # offset_seconds = client_time.utcoffset().total_seconds()
    # CLIENT_OFFSET = int(offset_seconds / 3600)  
    # return CLIENT_TIMEZONE, CLIENT_OFFSET



# def get_client_zone() -> int:
    # global CLIENT_OFFSET, CLIENT_TIMEZONE
    # timezone = datetime.now().astimezone().tzinfo
    # CLIENT_TIMEZONE = timezone    
# Получаем текущее время в этом часовом поясе
    # client_time = datetime.now(timezone)    
# Получаем смещение в секундах и переводим в часы
    # offset_seconds = client_time.utcoffset().total_seconds()
    # CLIENT_OFFSET = int(offset_seconds / 3600)    
    # return CLIENT_TIMEZONE, CLIENT_OFFSET 
# def get_client_zone() -> int:
    # global CLIENT_OFFSET, CLIENT_TIMEZONE
# Получение информации о местоположении пользователя через API
    # response = requests.get('https://ipinfo.io')
    # data = response.json()
    # tz_client = data['timezone']
# Создаем объект timezone из строки tz_client
    # timezone = pytz.timezone(tz_client)
    # CLIENT_TIMEZONE = timezone    
# Получаем текущее время в этом часовом поясе
    # client_time = datetime.now(timezone)    
# Получаем смещение в секундах и переводим в часы
    # offset_seconds = client_time.utcoffset().total_seconds()
    # CLIENT_OFFSET = int(offset_seconds / 3600)  
    # return CLIENT_TIMEZONE, CLIENT_OFFSET

 
# def get_client_time() -> datetime:
   ## return datetime.now(CLIENT_TIMEZONE)
   # server_time = get_server_time()
   # client_time = timedelta(hours=CLIENT_OFFSET)    
   # return client_time  
    
    
    # localized_now = localize_time(SERVER_TIMEZONE, now) 
    # localized_target_date = localize_time(SERVER_TIMEZONE, target_date)
    # print(f">>>>> localized_target_date: {localized_target_date}") 
    # now = get_client_time()
    
    # localized_user_stime = localize_time(SERVER_TIMEZONE, user_stime)
    # print(f"Show_time_ingame > localized_user_stime: {localized_user_stime}") 
    # localized_now = localize_time(SERVER_TIMEZONE, now)    
    # elapsed_time = localized_now - localized_user_stime 

         
    # hour = elapsed_time.hour
    # minute = elapsed_time.minute 
    # hour, remainder = divmod(elapsed_time.total_seconds(), 3600)
    # minute, second = divmod(remainder, 60)
    # hour = int(hour)
    # minute = int(minute)    
    # stime = format_time_ru(hour, minute)  
# Вариант с locale     # locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')    # return date.strftime('%B')    
# if sys.version_info >= (3, 9):
    # from zoneinfo import ZoneInfo
    # SERVER_TIMEZONE = ZoneInfo.from_system()
# else:
    # try:
        # from tzlocal import get_localzone
        # SERVER_TIMEZONE = get_localzone()
    # except ImportError:
        # from datetime import datetime
        # SERVER_TIMEZONE = datetime.now().astimezone().tzinfo
# print(f"Часовой пояс сервера: {SERVER_TIMEZONE}")  


# def get_client_zone() -> int:
    # global CLIENT_OFFSET, CLIENT_TIMEZONE    
    # Получаем локальное время системы
    # local_time = time_module.localtime()    
    # Вычисляем смещение от UTC в часах
    # utc_offset = local_time.tm_gmtoff / 3600
    # CLIENT_OFFSET = int(utc_offset)    
    # Находим соответствующую временную зону
    # for tz in pytz.all_timezones:
        # timezone = pytz.timezone(tz)
        # if timezone.utcoffset(datetime.now()) == timedelta(hours=CLIENT_OFFSET):
            # CLIENT_TIMEZONE = timezone
            # break    
    # return CLIENT_TIMEZONE, CLIENT_OFFSET   