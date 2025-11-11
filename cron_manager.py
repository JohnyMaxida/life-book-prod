# cron_manager.py
"""
Управление крон-задачами: напоминания, анализы, отчёты.
"""

from ai_manager import run_daily_reminder, run_evening_analysis, run_weekly_analysis
from marathon_logic import is_week_end
from report_manager import generate_and_send_report
from lifeman_new import get_day, save_day, getdb_time # For day management
from utils import Get_Var, Set_Var, Shot, S2TIME, days_passed # For utility functions
from const import MAX_DAYS, GEO # For constants
from datetime import datetime, timedelta, time # For date/time operations
import pytz
from pytz import FixedOffset
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
scheduler = AsyncIOScheduler() # Initialize scheduler globally
scheduler.start() # Start scheduler globally

# Словарь для хранения задач
cron_DATA = {}
life_Reminders = [   
    (time(14, 0), "alarm_freya_day"),
    (time(18, 0), "alarm_freya_evn"),
    (time(23, 50), "alarm_report")
] 

# Day management functions from active.py
async def Inc_Day(context: ContextTypes.DEFAULT_TYPE):
    text = Inc_Day_syn(context)
    # Assuming SEX is in ui_blocks.py
    from ui_blocks import SEX
    return await SEX(text, context)

def Inc_Day_syn(context: ContextTypes.DEFAULT_TYPE):
    user_id = Get_Var('user_id', context)
    new_day = get_day(user_id) + 1
    if new_day >= MAX_DAYS:
        print("Охренеть, дней больше чем массив! Начинаем сначала.")
        new_day = 1
    print(f">INC> Новый день: {new_day}")
    save_day(new_day, user_id)
    text = f"Ура 🌟 Поздравляю Вас с началом Нового дня {new_day} 😊\n✳️ Сделайте растарт бота по команде /start"
    return text

def AUTODAY(context: ContextTypes.DEFAULT_TYPE):
    user_id = Get_Var('user_id', context)
    user_stime = getdb_time(user_id)
    if user_stime is None:
        print("CRON >1< Первый Вход в Игру (1) Запускаем МАРАФОН")
        now = datetime.utcnow() # Use UTC for initial save
        print(f"CRON >1< Время старта зафиксировано: {Shot(now)}")
        save_day(1, user_id) # Start with day 1
        savedb_time(now, user_id)
        Set_Var('user_stime', now, context)
        return 1
    else:
        Set_Var('user_stime', user_stime, context)
        start_obj = S2TIME(user_stime) if isinstance(user_stime, str) else user_stime
        if GEO:
            start_obj = start_obj.replace(hour=0, minute=0, second=0, microsecond=0)
        days_pass = days_passed(start_obj)
        shorts = Shot(user_stime)
        Set_Var('day_pass', days_pass, context)
        print(f"CRON >1< Игра стартовала: {shorts}")
        print(f"CRON >1< Прошло дней: {days_pass} ")
        current_day = get_day(user_id)
        if days_pass > 0 and (current_day != days_pass + 1):
            print(f"> Нужен Перерасчет День:{current_day} Пасс:{days_pass} (3)")
            # Set_Var('day', days_pass, context) # This is handled by Inc_Day_syn
            Inc_Day_syn(context)
            return True
        else:
            print("> Нет повода инкременации (0)")
            return False


async def schedule_crons(application):
    """Регистрирует все крон-задачи в приложении."""
    from telegram.ext import ContextTypes
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    from const import CRON_ALARM_TIME, CRON_EVENING_TIME, CRON_REPORT_TIME

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    async def wrap_flow(flow_func, context: ContextTypes.DEFAULT_TYPE):
        try:
            await flow_func(context)
        except Exception as e:
            print(f"Ошибка в крон-задаче: {e}")

    # Ежедневное напоминание в 14:00
    scheduler.add_job(
        lambda ctx: wrap_flow(run_daily_reminder, ctx),
        CronTrigger.from_crontab(CRON_ALARM_TIME.replace(':', ' ')),
        misfire_grace_time=300
    )

    # Вечерний анализ в 18:00
    scheduler.add_job(
        lambda ctx: wrap_flow(run_evening_analysis, ctx),
        CronTrigger.from_crontab(CRON_EVENING_TIME.replace(':', ' ')),
        misfire_grace_time=300
    )

    # Ежедневный отчёт в 21:00
    scheduler.add_job(
        lambda ctx: wrap_flow(lambda c: generate_and_send_report(c, final=False), ctx),
        CronTrigger.from_crontab(CRON_REPORT_TIME.replace(':', ' ')),
        misfire_grace_time=300
    )

    scheduler.start()
    application.job_queue.scheduler = scheduler
