# AMBACRON
"""
DEPRECATED MODULE - This module is deprecated and scheduled for removal.
All cron functionality has been migrated to cron_manager.py.

This file is kept temporarily for reference but should not be used.
Use cron_manager.py instead.
"""
# ⚠️ WARNING: This module uses old Telegram API and is DEPRECATED
# ⚠️ All functions have been moved to cron_manager.py
# ⚠️ This file will be removed in future versions

from telegram import Update
from telegram.ext import ContextTypes
from lifeman import getdb_time, savedb_time, get_timezone
from active import Inc_Day_syn, Get_User_Day
from datetime import datetime, timedelta, time
from temporal import *
from passive import Get_Var, Set_Var, Get_Uid, UMR, ESU, SEX
# , TextBlock
import pytz
from pytz import FixedOffset
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
scheduler = AsyncIOScheduler()
scheduler.start()

GEO = 1
# Словарь для хранения задач
cron_DATA = {}
life_Reminders = [   
    (time(14, 0), "alarm_freya_day"),
    (time(18, 0), "alarm_freya_evn"),
    (time(23, 50), "alarm_report")
    # (time(9, 0), "warn_morning"),
    # (time(18, 0), "warn_evening"),
    # (time(0, 1), "alarm_increment")
] 

def CRON_AMBA1(context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    chat_id = Get_Uid(context)
    day = Get_User_Day(context)     
    user_stime = getdb_time()  
    now = get_server_time()     
    print("CRON >1< Время по серверу: ", now)  

    if user_stime is None:
        print("CRON >1< Первый Вход в Игру (1) Запускаем МАРАФОН")
        print(f"CRON >1< Время старта зафиксировано: {shot(now)}")
        savedb_time(now)
        Set_Var('user_stime', now, context)        
        return 1
    else:
        Set_Var('user_stime', user_stime, context)
        start_obj = S2TIME(user_stime)    
        if GEO:
            start_obj = start_obj.replace(hour=0, minute=0, second=0)
        days_pass = days_passed(start_obj)
        shorts = shot(user_stime)
        Set_Var('day_pass', days_pass, context)
        print(f"CRON >1< Игра стартовала: {shorts}")
        print(f"CRON >1< Прошло дней: {days_pass} ")        
        # celc = True
        # CRON_AMBA2(context) # целкостный - 1 вход в день
        # if celc:
            
        if days_pass>0 and (day != days_pass+1):
            print(f"> Нужен Перерасчет День:{day} Пасс:{days_pass} (3)")
            # Set_Var('day', days_pass, context)
            # Inc_Day_syn(context)
            return True
        else:    
            # Inc_Day_syn(context) 
            print("> Нет повода инкременации (0)")
            return False
        # else:         
            # print("Повторный вход > Нет повода инкременации дня (0)")
            # return 0

def CRON_AMBA2(context: ContextTypes.DEFAULT_TYPE):
    flag = False
    print("CRON_REM > АКТИВИРУЕМ для контроля Домашки")
    for r_time, r_name in life_Reminders:
        rez = add_task(r_name, r_time, context)
        if not 'CRON-ATS' in rez:
           flag = True 
    print("CRON_REM > напоминалки проверены и обновлены")
    return flag

async def Crons_TEST(r_name: str, context: ContextTypes.DEFAULT_TYPE):
    try:
        await run_sched(r_name, context)
        await SEX(f"Задача '{r_name}' успешно выполнена.", context)
    except Exception as e:
        await SEX(f"Произошла ошибка при выполнении задачи '{r_name}': {str(e)}", context)

async def run_sched(task_name: str, context: ContextTypes.DEFAULT_TYPE):
    chat_id = Get_Uid(context)
    print("CRON-RunShred > ", task_name, end='')
    if task_name not in cron_DATA:
        text = f" > Неизвестная задача: {task_name}"
        print(text)
        return text
    print(f" >> Выполнение задачи: {task_name}")
    now = get_server_time()
    nows = T2str(now)
    data = cron_DATA[task_name]
    task_info = f"""
    CRON_RUN >>> Информация о задаче:
    Имя CRON задачи: {task_name}
    Имя DATA задачи: {data['task_name']}
    Время запуска задачи: {data['task_time']}
    Время запуска строка: {data['task_times']}
    Время NOW задачи: {data['now']}
    Время NOW строка: {data['nows']}
    Часовой пояс юзера: {data['user_tz']}
    Дата-Время задачи: {data['task_datetime']}
    Дата-Время строка: {data['task_datetimes']}
    UTC-Время задачи: {data['utc_task_time']}
    UTC-Время строка: {data['utc_task_times']}    
    Текущее время: {now}
    Текущее время строка: {nows}
    Chat ID: {chat_id}
    """   
    print(task_info)
    # await SEX(task_info, context)    
    if task_name.startswith("warn_"):
        await Day_Alarm(task_name, context)
    elif task_name.startswith("alarm_"):
        await Alarm_RUN(task_name, context)  # Добавлен await здесь

def add_task(r_name: str, r_time: time, context: ContextTypes.DEFAULT_TYPE):
    if r_name in cron_DATA:
        return f"CRON-ATS >>> Задача '{r_name}' - уже стоит - пропускаем"
    chat_id = Get_Uid(context)
    # from lifeman import get_timezone
    user_zone = get_timezone() or 0
    if isinstance(r_time, datetime):
        r_time = r_time.time()      
    offset_minutes = int(user_zone) * 60
    user_tz = FixedOffset(offset_minutes)
    now = datetime.now(user_tz)
    task_datetime = user_tz.localize(datetime.combine(now.date(), r_time))
    utc_task_time = task_datetime.astimezone(pytz.UTC)
    now = datetime.now(user_tz)
    nows = T2str(now)
    rtimes = T2str(r_time)
    task_datetimes  = T2str(task_datetime)
    utc_task_times  = T2str(utc_task_time)    
    data = {
        'task_name': r_name,
        'task_time': r_time,
        'task_times': rtimes,
        'now': now,
        'nows': nows,
        'user_tz': user_tz,
        'task_datetime': task_datetime,
        'task_datetimes': task_datetimes,
        'utc_task_time': utc_task_time,
        'utc_task_times': utc_task_times
    }
    cron_DATA[r_name] = data  
    scheduler.add_job(
        run_sched,
        CronTrigger(
            hour=utc_task_time.hour, 
            minute=utc_task_time.minute, 
            timezone=pytz.UTC
        ),
        id=r_name,
        args=[r_name, context]
    )    
    return f"CRON-AddShred > Задача '{r_name}' добавлена на {rtimes} ()."

def edit_task(r_name: str, new_time: time, context: ContextTypes.DEFAULT_TYPE):
    chat_id = Get_Uid(context)
    if r_name in cron_DATA:
        remove_task(r_name)
        result = add_task(r_name, new_time, context)
        return f"> Задача '{r_name}' перенесена на {T2str(new_time)}"
    else:
        return f"> Задача '{r_name}' не найдена."

def remove_task(r_name: str):
    if r_name in cron_DATA:
        scheduler.remove_job(r_name)
        del cron_DATA[r_name]
        return f"> Задача '{r_name}' удалена."
    else:
        return f"> Задача '{r_name}' не найдена."



# async def Day_Alarm(task_name, context: ContextTypes.DEFAULT_TYPE):
    # warn = "Пора бы выполнить домашнее задание!"
    # warns = ["warn_morning", "warn_dinner", "warn_evening"]
    # print(warn)
    # if task_name in warns:
        # warn = TextBlock(task_name)
        # await SEX(warn, context)
        
async def Adaily_increment(context: ContextTypes.DEFAULT_TYPE):
    message = "adaily_increment >>> Запущен плановый инкременатор дня"
    print(message)
    await SEX(message, context)   


async def Alarm_Freya_day(context: ContextTypes.DEFAULT_TYPE):
    from logical import FREYA_DAYJOB
    message = ">>> Запущена процедура ФРЕЯ - дневная напоминалка"
    print(message)  
    await FREYA_DAYJOB(context)
    
    
async def Alarm_Freya_even(context: ContextTypes.DEFAULT_TYPE):
    from logical import FREYA_EVENING
    message = ">>> Запущена процедура ФРЕЯ - анализ задания вечера"
    print(message)  
    await FREYA_EVENING(context)    
    

async def Alarm_Report(context: ContextTypes.DEFAULT_TYPE):
    from logical import TEST_EVENING
    message = ">>> Запущена процедура проверки заполнения дневника >"
    print(message, end='')  
    result = await TEST_EVENING(context)
    print(result)  

async def Alarm_RUN(msg:str, context: ContextTypes.DEFAULT_TYPE):
    message = "Alarm_RUN >>> Запущен селектор рабочих команд кронтаба"
    print(message)
    # await SEX(message, context)
    cut = msg.replace('alarm_','')
    if cut == 'freya_day':
        await Alarm_Freya_day(context)
    elif cut == 'freya_evn':
        await Alarm_Freya_even(context)        
    elif 'report' in cut:
        await Alarm_Report(context)

def cron_tasks(update, context: ContextTypes.DEFAULT_TYPE):
    if not cron_DATA:
        return [], "CRON-T >>> Нет активных задач"    
    task_arr = [[r_name, data['task_times']] for r_name, data in cron_DATA.items()]
    task_str = pluralize_ru(len(cron_DATA), "задача", "задачи", "задач")    
    task_list = f"Активные {task_str}:\n" + "\n".join([f"{ESU(name)} в {time}" for name, time in task_arr])
    print(f"CRON >>> {task_list}")
    return task_arr, task_list