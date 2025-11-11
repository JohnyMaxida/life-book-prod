# cron_manager.py
"""
Управление крон-задачами: напоминания, анализы, отчёты.
Refactored for aiogram 3.x
"""

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta, time
import pytz
from pytz import FixedOffset
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from ai_manager import run_daily_reminder, run_evening_analysis, run_weekly_analysis
from marathon_logic import is_week_end
from report_manager import generate_and_send_report
from lifeman import get_day, save_day, getdb_time, savedb_time
from utils import Shot, S2TIME, days_passed
from const import MAX_DAYS, GEO
from logger import logger

# Initialize scheduler globally
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

# Словарь для хранения задач
cron_DATA = {}
life_Reminders = [
    (time(14, 0), "alarm_freya_day"),
    (time(18, 0), "alarm_freya_evn"),
    (time(23, 50), "alarm_report")
]

# Day management functions
async def Inc_Day(user_id: int, bot: Bot):
    """Increment user day and send notification."""
    text = await Inc_Day_syn(user_id)
    await bot.send_message(user_id, text)
    return text

async def Inc_Day_syn(user_id: int) -> str:
    """Increment user day synchronously and return message."""
    current_day = await get_day(user_id)
    new_day = current_day + 1
    if new_day >= MAX_DAYS:
        logger.warning(f"User {user_id} reached max days, resetting to day 1")
        new_day = 1
    logger.info(f"User {user_id}: Incrementing day to {new_day}")
    await save_day(user_id, new_day)
    text = f"Ура 🌟 Поздравляю Вас с началом Нового дня {new_day} 😊\n✳️ Сделайте рестарт бота по команде /start"
    return text

async def AUTODAY(user_id: int, state: FSMContext) -> int:
    """
    Auto-increment day based on time passed since game start.
    Returns: 1 if first entry, True if day incremented, False if no increment needed
    """
    user_stime = await getdb_time(user_id)

    if user_stime is None:
        logger.info(f"User {user_id}: First game entry, starting marathon")
        now = datetime.utcnow()  # Use UTC for initial save
        logger.info(f"User {user_id}: Start time fixed at {Shot(now)}")
        await save_day(user_id, 1)  # Start with day 1
        await savedb_time(user_id, now)
        await state.update_data(user_stime=now)
        return 1
    else:
        await state.update_data(user_stime=user_stime)
        start_obj = S2TIME(user_stime) if isinstance(user_stime, str) else user_stime

        if GEO:
            start_obj = start_obj.replace(hour=0, minute=0, second=0, microsecond=0)

        days_pass = days_passed(start_obj)
        shorts = Shot(user_stime)
        await state.update_data(day_pass=days_pass)

        logger.info(f"User {user_id}: Game started at {shorts}")
        logger.info(f"User {user_id}: Days passed: {days_pass}")

        current_day = await get_day(user_id)
        if days_pass > 0 and (current_day != days_pass + 1):
            logger.info(f"User {user_id}: Day recalculation needed. Current: {current_day}, Passed: {days_pass}")
            await Inc_Day_syn(user_id)
            return True
        else:
            logger.debug(f"User {user_id}: No day increment needed")
            return False


async def schedule_crons(bot: Bot):
    """Register all cron tasks for the bot."""
    from const import CRON_ALARM_TIME, CRON_EVENING_TIME, CRON_REPORT_TIME

    async def wrap_flow(flow_func):
        """Wrapper for cron job error handling."""
        try:
            await flow_func(bot)
        except Exception as e:
            logger.error(f"Error in cron task: {e}", exc_info=True)

    # Daily reminder at 14:00
    scheduler.add_job(
        lambda: wrap_flow(run_daily_reminder),
        CronTrigger.from_crontab(CRON_ALARM_TIME.replace(':', ' ')),
        misfire_grace_time=300
    )

    # Evening analysis at 18:00
    scheduler.add_job(
        lambda: wrap_flow(run_evening_analysis),
        CronTrigger.from_crontab(CRON_EVENING_TIME.replace(':', ' ')),
        misfire_grace_time=300
    )

    # Daily report at 21:00
    scheduler.add_job(
        lambda: wrap_flow(lambda b: generate_and_send_report(b, final=False)),
        CronTrigger.from_crontab(CRON_REPORT_TIME.replace(':', ' ')),
        misfire_grace_time=300
    )

    scheduler.start()
    logger.info("Cron scheduler started successfully")
