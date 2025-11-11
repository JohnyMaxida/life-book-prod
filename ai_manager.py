"""
AI Manager for Life-Book Bot.
Handles all high-level AI interactions (FREYA) using free11ray as driver.
"""
import asyncio
from typing import Optional
from telegram.ext import ContextTypes
from const import AIPrompts
from free11ray import INHA_TEX
from lifeman_new import get_day, Get_User_Day, Get_day_responses, get_question


from free11ray import INHA_TEX, AIQue
from const import AIPrompts
from lifeman_new import get_user_responses, Get_User_Day, Get_Var

async def run_daily_reminder(context):
    name = Get_Var('user_nick', context)
    day = Get_User_Day(context)
    responses = get_user_responses()
    count = sum(1 for r in responses[:3] if r)
    warning = "\nИгрок даже не приступал!" if count == 0 else ""
    prompt = AIPrompts.DAILY_REMINDER.format(name=name, count=count, warning=warning)
    return await INHA_TEX(prompt, f"[name={name}]", context)

async def run_evening_analysis(context):
    name = Get_Var('user_nick', context)
    day = Get_User_Day(context)
    responses = get_user_responses()
    answer = responses[2] if len(responses) > 2 else None
    if not answer:
        return
    question = get_question(day)  #  нужно вынести в marathon_logic или utils
    prompt = AIPrompts.EVENING_ANALYSIS.format(name=name, question=question, answer=answer)
    return await INHA_TEX(prompt, "", context)

async def run_weekly_analysis(context):
    name = Get_Var('user_nick', context)
    all_answers = get_all_responses()  #  реализовать в lifeman_new или marathon_logic
    prompt = AIPrompts.WEEK_ANALYSIS.format(name=name, answers=all_answers)
    return await INHA_TEX(prompt, "", context)

# Добавить: run_final_analysis, run_custom_freya_request и т.д.



async def freya_day_reminder(context: ContextTypes.DEFAULT_TYPE) -> str:
    """14:00 - напоминание о незаполненном дневнике."""
    user_nick = context.user_data.get('user_nick', 'Игрок')
    day = Get_User_Day(context)
    responses = Get_day_responses(day)
    count = sum(1 for r in responses[:3] if r) if responses else 0

    warning = ""
    if count < 3:
        warning = "\n?Вы ещё не заполнили все ответы на сегодня."

    prompt = AIPrompts.DAILY_REMINDER.format(
        name=user_nick,
        count=count,
        warning=warning
    )
    return await INHA_TEX(prompt, '', context)


async def freya_evening_analysis(context: ContextTypes.DEFAULT_TYPE) -> str:
    """18:00 - анализ главного (3-го) ответа дня."""
    user_nick = context.user_data.get('user_nick', 'Игрок')
    day = Get_User_Day(context)
    responses = Get_day_responses(day)

    if not responses or not responses[2]:
        return ""

    question = get_question(day) or "Вопрос не задан"
    answer = responses[2]

    prompt = AIPrompts.EVENING_ANALYSIS.format(
        name=user_nick,
        question=question,
        answer=answer
    )
    return await INHA_TEX(prompt, '', context)


async def freya_weekly_review(context: ContextTypes.DEFAULT_TYPE) -> str:
    """После 7-го дня - недельный разбор."""
    user_nick = context.user_data.get('user_nick', 'Игрок')
    all_responses = []
    for d in range(1, 8):
        day_resp = Get_day_responses(d)
        if day_resp:
            for i, resp in enumerate(day_resp[:3]):
                if resp:
                    q = get_question(d) if i == 2 else const.TASKS[i]
                    all_responses.append(f"День {d}, {q}\n{resp}\n")
    answers = "\n".join(all_responses) if all_responses else "Ответы отсутствуют"

    prompt = AIPrompts.WEEK_ANALYSIS.format(
        name=user_nick,
        answers=answers
    )
    return await INHA_TEX(prompt, '', context)


async def freya_custom_request(prompt: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Ручной запрос от пользователя (step=25)."""
    user_nick = context.user_data.get('user_nick', 'Игрок')
    user_context = f"[name={user_nick}]"
    return await INHA_TEX(prompt, user_context, context)


# Утилиты для формирования промптов (опционально вынести в utils, но пока здесь