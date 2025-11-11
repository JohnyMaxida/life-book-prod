# media_handler.py
"""
Обработка медиа: аудио, видео → текст.
Refactored for aiogram 3.x
"""

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from fre0lib import Transcribe_audio
from ui_blocks import SEX
from lifeman import Update_task_response, Get_User_Day
from const import Steps


async def handle_voice_message(message: Message, state: FSMContext):
    """
    Handle voice messages from users.
    Transcribes audio to text and processes based on current step.

    Args:
        message: Aiogram Message object containing voice
        state: FSMContext for user state storage
    """
    voice = message.voice
    if not voice:
        return

    user_id = message.from_user.id
    file_id = voice.file_id

    # Get user nickname from state
    user_data = await state.get_data()
    user_nick = user_data.get('user_nick', 'user')

    # Send processing message
    await message.answer("🎙 Распознавание голоса...")

    # Transcribe audio (note: fre0lib.Transcribe_audio may need refactoring)
    text = await Transcribe_audio(user_nick, file_id, message.bot)
    if "err:" in text:
        await message.answer("❌ Ошибка распознавания.")
        return

    # If user is on input task answer step, save the response
    current_step = user_data.get('step')
    if current_step == Steps.INPUT_TASK_ANSWER:
        day = await Get_User_Day(user_id)
        task_index = user_data.get('cur_task', 0)
        await Update_task_response(user_id, task_index, day, text)
        await message.answer("✅ Ответ сохранён!")
    else:
        await message.answer(f"Вы сказали: {text}")