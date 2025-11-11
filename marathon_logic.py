# marathon_logic.py
"""
Логика марафона: прогресс дня/недели, проверка ДЗ, бонусы, переходы.
"""

from lifeman import (
    Get_user_responses,
    get_credos,
    save_credos,
    get_day,
    save_day,
    get_uweek,
    save_uweek,
    Get_DOLE_FP,
    Set_DOLE_FP,
    Inc_Lives,
    Inc_Vitas,
    save_pays, # Added for grant_premium_access
    save_role, # Added for grant_premium_access
    get_role # Added for grant_premium_access
)
from db_manager import DatabaseManager # Import DatabaseManager
from aiogram import Bot # Import Bot for functions that send messages
from const import MAX_DAYS, TASKS


async def check_homework(user_id: int, db_manager: DatabaseManager) -> bool:
    """Проверяет, выполнено ли хотя бы одно задание."""
    day = await get_day(user_id)
    responses = await Get_user_responses(user_id)
    # Assuming TASKS is a list of task IDs or similar, and responses is a dict of {task_id: response_text}
    # This logic needs to be refined based on the actual structure of TASKS and responses
    task_flags = [bool(responses.get(str(i))) for i in range(len(TASKS))] # Assuming TASKS is a list of 3 tasks
    return any(task_flags)


async def is_all_tasks_done(user_id: int, db_manager: DatabaseManager) -> bool:
    """Проверяет, заполнены ли все 3 задания."""
    responses = await Get_user_responses(user_id)
    # Assuming TASKS is a list of 3 tasks and responses is a dict of {task_id: response_text}
    return all(responses.get(str(i)) for i in range(len(TASKS)))


async def inc_day_if_complete(user_id: int, db_manager: DatabaseManager) -> None:
    """Увеличивает день, если все задания выполнены."""
    if await is_all_tasks_done(user_id, db_manager):
        current = await get_day(user_id)
        if current < MAX_DAYS:
            await save_day(user_id, current + 1)
            # Сброс защёлки для начисления доли
            await Set_DOLE_FP(user_id, False)


async def is_week_end(user_id: int, db_manager: DatabaseManager) -> bool:
    """Проверяет, завершилась ли неделя (7-й день)."""
    dole = await get_credos(user_id, 4) # Assuming 4 is the index for 'Doles'
    return dole == 7


async def is_final_day(user_id: int, db_manager: DatabaseManager) -> bool:
    """Проверяет, достигнут ли последний день марафона."""
    return await get_day(user_id) >= MAX_DAYS


async def handle_week_end(user_id: int, db_manager: DatabaseManager) -> None:
    """Начисляет бонусы за завершение недели."""
    if not await Get_DOLE_FP(user_id):
        await Inc_Lives(user_id, lives=1)
        await Inc_Vitas(user_id, vitas=1)
        week = await get_uweek(user_id)
        await save_uweek(user_id, week + 1)
        await Set_DOLE_FP(user_id, True)


async def grant_premium_access(user_id: int, db_manager: DatabaseManager) -> None:
    """Даёт доступ к PRO-функциям после оплаты."""
    role = await get_role(user_id)
    if "+" not in role:
        await save_role(user_id, role + "+")
    await save_pays(user_id, 1)  # или индекс тарифа
