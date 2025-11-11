# media_handler.py
"""
Обработка медиа: аудио, видео → текст.
"""

from fre0lib import Transcribe_audio, SEX
from lifeman_new import Update_task_response, Get_User_Day
from const import Steps


async def handle_voice_message(update, context):
    voice = update.message.voice
    if not voice:
        return

    user_id = update.effective_user.id
    file_id = voice.file_id
    user_nick = context.user_data.get('user_nick', 'user')

    await SEX("🎙 Распознавание голоса...", update.effective_chat.id, context)

    text = await Transcribe_audio(user_nick, file_id, context)
    if "err:" in text:
        await SEX("❌ Ошибка распознавания.", update.effective_chat.id, context)
        return

    # Если пользователь находится на шаге ввода ответа — сохраняем
    if context.user_data.get('step') == Steps.INPUT_TASK_ANSWER:
        day = Get_User_Day(context)
        task_index = context.user_data.get('cur_task', 0)
        Update_task_response(task_index, day, text)
        await SEX("✅ Ответ сохранён!", update.effective_chat.id, context)
    else:
        await SEX(f"Вы сказали: {text}", update.effective_chat.id, context)