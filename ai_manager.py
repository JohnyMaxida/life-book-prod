"""
AI Manager for Life-Book Bot.
Handles all high-level AI interactions (FREYA) using free11ray as driver.
Migrated to aiogram 3.x - preserving all AI logic intact.
"""
import asyncio
from typing import Optional
from aiogram.fsm.context import FSMContext
from const import AIPrompts
from free11ray import INHA_TEX, AIQue
from lifeman_new import get_day, Get_User_Day, Get_day_responses, get_question, get_user_responses
from utils import Get_Var

async def run_daily_reminder(state: FSMContext):
    """
    Run daily reminder for user (14:00).

    Args:
        state: FSMContext for user state management

    Returns:
        AI-generated reminder message
    """
    name = await Get_Var('user_nick', state)
    day = Get_User_Day(state)
    responses = get_user_responses()
    count = sum(1 for r in responses[:3] if r)
    warning = "\nСрок сдачи не наступает!" if count == 0 else ""
    prompt = AIPrompts.DAILY_REMINDER.format(name=name, count=count, warning=warning)
    return await INHA_TEX(prompt, f"[name={name}]", state)

async def run_evening_analysis(state: FSMContext):
    """
    Run evening analysis for user (18:00).

    Args:
        state: FSMContext for user state management

    Returns:
        AI-generated evening analysis
    """
    name = await Get_Var('user_nick', state)
    day = Get_User_Day(state)
    responses = get_user_responses()
    answer = responses[2] if len(responses) > 2 else None
    if not answer:
        return
    question = get_question(day)
    prompt = AIPrompts.EVENING_ANALYSIS.format(name=name, question=question, answer=answer)
    return await INHA_TEX(prompt, "", state)

async def run_weekly_analysis(state: FSMContext):
    """
    Run weekly analysis for user (after day 7).

    Args:
        state: FSMContext for user state management

    Returns:
        AI-generated weekly analysis
    """
    name = await Get_Var('user_nick', state)
    all_answers = get_all_responses()
    prompt = AIPrompts.WEEK_ANALYSIS.format(name=name, answers=all_answers)
    return await INHA_TEX(prompt, "", state)

async def freya_day_reminder(state: FSMContext) -> str:
    """
    14:00 - Daily reminder with task progress.

    Args:
        state: FSMContext for user state management

    Returns:
        AI-generated reminder message
    """
    data = await state.get_data()
    user_nick = data.get('user_nick', 'Игрок')
    day = Get_User_Day(state)
    responses = Get_day_responses(day)
    count = sum(1 for r in responses[:3] if r) if responses else 0

    warning = ""
    if count < 3:
        warning = "\nТы еще не ответил на ответы на сегодня."

    prompt = AIPrompts.DAILY_REMINDER.format(
        name=user_nick,
        count=count,
        warning=warning
    )
    return await INHA_TEX(prompt, '', state)

async def freya_evening_analysis(state: FSMContext) -> str:
    """
    18:00 - Evening analysis of user's answer.

    Args:
        state: FSMContext for user state management

    Returns:
        AI-generated evening analysis
    """
    data = await state.get_data()
    user_nick = data.get('user_nick', 'Игрок')
    day = Get_User_Day(state)
    responses = Get_day_responses(day)

    if not responses or not responses[2]:
        return ""

    question = get_question(day) or "вопрос дня"
    answer = responses[2]

    prompt = AIPrompts.EVENING_ANALYSIS.format(
        name=user_nick,
        question=question,
        answer=answer
    )
    return await INHA_TEX(prompt, '', state)

async def freya_weekly_review(state: FSMContext) -> str:
    """
    After day 7 - Weekly review.

    Args:
        state: FSMContext for user state management

    Returns:
        AI-generated weekly review
    """
    data = await state.get_data()
    user_nick = data.get('user_nick', 'Игрок')
    all_responses = []
    for d in range(1, 8):
        day_resp = Get_day_responses(d)
        if day_resp:
            for i, resp in enumerate(day_resp[:3]):
                if resp:
                    from const import TASKS
                    q = get_question(d) if i == 2 else TASKS[i]
                    all_responses.append(f"День {d}, {q}\n{resp}\n")
    answers = "\n".join(all_responses) if all_responses else "Ответов недостаточно"

    prompt = AIPrompts.WEEK_ANALYSIS.format(
        name=user_nick,
        answers=answers
    )
    return await INHA_TEX(prompt, '', state)

async def freya_custom_request(prompt: str, state: FSMContext) -> str:
    """
    Custom AI request from user (step=25).

    Args:
        prompt: User's custom prompt
        state: FSMContext for user state management

    Returns:
        AI-generated response
    """
    data = await state.get_data()
    user_nick = data.get('user_nick', 'Игрок')
    user_context = f"[name={user_nick}]"
    return await INHA_TEX(prompt, user_context, state)
