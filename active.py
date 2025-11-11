# ACTIVE
# Refactored to aiogram 3.x - Step 4
# Import specific functions from passive.py instead of wildcard import

import os, io, requests
from datetime import datetime
from pydub import AudioSegment
import speech_recognition as sr
from aiogram.fsm.context import FSMContext
from aiogram import Bot

# Import specific functions from passive instead of wildcard
from passive import (CYFER, IsUserPREM, IsUserPreme, IsPREM, get_tariff_info,
                     get_tariff_infoby_index, TARIFS, Send_Stik)
from lifeman import *
from answers import Update_task_response, Get_task_response, Init_Answers
from temporal import Show_Game_Time, S2TIME, pluralize_ru, Adelay
from utils import Get_Uid, Get_Var, Get_VAR, Set_Var
from ui_blocks import SEX

# Import duplicate functions from cron_manager (these were duplicated here)
# Note: Inc_Day, Inc_Day_syn, AUTODAY are now in cron_manager.py

# status_smiles = ['❌','🙋🏼','👌🏻','🙅🏼','✅']
MAX_DAYS = 28
LANG_CODE = "ru-RU"
Start_Time:datetime = None

def Ext_SS(stat_string):
    """Extract status with smile and newline."""
    smile = stat_string[0]
    return smile+"\n"+stat_string

def Ext_SSS(stat_string, SYM):
    """Extract status with smile, newline and surrounding symbols."""
    smile = stat_string[0]
    return smile+"\n"+SYM+stat_string+SYM

def Ext_BS(stat_string):
    """Extract bold status (* surrounding)."""
    return Ext_SSS(stat_string, '*')

def Ext_CS(stat_string):
    """Extract code status (_ surrounding)."""
    return Ext_SSS(stat_string, '_')

def Ext_TS(stat_string):
    """Extract teletype status (` surrounding)."""
    return Ext_SSS(stat_string, '`')

def Form_Port(findex, value) -> str:
    """
    Format report string by format index.

    Args:
        findex: Format index (1-98)
        value: Value to insert into format

    Returns:
        str: Formatted report string
    """
    forma = ''
    if findex==1:    # шапка 1 standart
        forma = f"⚜️ *ИНФОРМАЦИЯ ОБ ИГРОКЕ* 💁🏻‍♂️ {value}"
    elif findex==10: # шапка 10
        forma = f"📗 ДАННЫЕ ПОЛЬЗОВАТЕЛЯ:{value}"
    elif findex==11: # шапка 11 старт
        forma = "🧾 ОТЧЕТ -Д.З- ИГРОКА 💁🏻‍♂️"
    elif findex==12: # шапка мд1
        forma = "🙋🏼 МЕНЮ МОДЕРАТОРА 📊 ОТЧЕТ:"
    elif findex==13: # шапка мд2
        forma = "🙋🏼 МОДЕРАТОР 👉🏻 АРХИВ 📊 и журналы отчета:"
    elif findex==14: # шапка мд3
        forma = "🙋🏼 МЕНЮ МОДЕРАТОРА 🙅🏼 ВВЕДИТЕ ПРИЧИНУ ОТКАЗА:"
    elif findex==15: # шапка мд4
        forma = "🙋🏼 МОДЕРАТОР 🧩 РАПОРТ ОБ ОШИБКЕ:"
    elif findex==16: # шапка 7+1 LONG
        forma = "👁СИНХРО-ШПИОН 😎 РАПОРТ ОБ ОШИБКЕ"
    elif findex==17: # шапка 7+2 short
        forma = f"👁ШПИОН👁 > {value}"
    elif findex==18: # шапка 7+3 short
        forma = f"👁ШПИОН{value}"
    elif findex==19: # шапка 7+4 short
        forma = "👁ШПИОН👁 > Обновление бота у Юзера:"
    elif findex==2: # имя
        forma = f"👤 Псевдоним пользователя: {value}"
    elif findex==21: # СИС.СТАТУС
        forma = f"🗿 Ранг пользователя: {value}"
    elif findex==22: # 🙋🏼 МЕНЮ МОДЕРАТОРА
        forma = "🧩 КОНСОЛЬ МОДЕРАТОРА 🧩"
    elif findex==23: # имя2
        forma = f"👤 Псевдоним игрока: {value}"
    elif findex==24: # задач сделано
        forma = f"☑️ Задач выполнено: {value}"
    elif findex==25: # 📟 Консоль контроля ДЗ
        forma = "📟 Консоль Контроля ДЗ 📟"
    elif findex==3: # день 1
        forma = f"📅 ДЕНЬ задания: {value}й день"
    elif findex==31: # задач в день
        forma = f"🔢 Задач на день: {value}"
    elif findex==33: # день 2
        forma = f"📅 *ДЕНЬ задания:* 🌘{value}🌒 "
    elif findex==34: # день 3
        value_s = CYFER(str(value))
        forma = f"📅 *ДЕНЬ задания:* {value}й🌘{value_s}"

    elif findex==26: # 🙋🏼 МЕНЮ МОДЕРАТОРА
        forma = "🧩 КОНСОЛЬ ОПЛАТЫ 🧩"
    elif findex==4: # айди
        forma = f"🆔 ID игрока: {value}"
    elif findex==5: # статус
        forma = f"🎠 Статус Дня: {value}"
    elif findex==51: # статус ДНЯ
        forma = f"🎠 Статус {value} Дня: "
    elif findex==6: # файл отчета
        value = os.path.basename(value)
        forma = f"📊 ФАЙЛ ОТЧЕТА: {value}"
    elif findex==61: # файл архив отчета
        value = os.path.basename(value)
        forma = f"📊 ФАЙЛ ОТЧЕТА: архив 🧾 {value}"
    elif findex==62: # голосовые сообщения
        forma = f"🗣 Голосовые сообщения: {value} шт."
    elif findex==63: # кол-во задач
        forma = f"📜 Число задач данного дня: {value} из 9"
    elif findex==7: # время
        forma = "⌛ Игра еще не запущена..." if (value is None) else f"⌛ Время в Игре: {value}"
    elif findex==81: # БАЛЛЫ
        forma = f"БАЛЛЫ:{value}🏆"  # +1
    elif findex==82: # ЖИЗНИ
        forma = f"ЖИЗНИ:{value}💖"  # +2
    elif findex==83: # АТЛ
        forma = f"АТЛЫ:{value}💵"  # +3
    elif findex==88: # РЕСУРСЫ
        forma = f"💰 *ИГРОВЫЕ РЕСУРСЫ:* {value}"  # +все
    elif findex==9: # КОД
        forma = f"🔑 Ваш личный реферальный ключ: {value}"
    elif findex==91: # ССЫЛКА
        forma = f"📩 Ваша личная реферальная ссылка: {value}"
    elif findex==92: # REF.count
        forma = f"👥 Количество рефералов: {value}"
    elif findex==93: # REF.count1
        forma = f"👥 Кол-во рефералов 1 уровня: {value}"
    elif findex==94: # REF.count2
        forma = f"👥 Кол-во рефералов 2 уровня: {value}"
    elif findex==95: # REF.rate
        forma = f"🥇 Реферальный рейтинг: {value}"
    elif findex==96: # REF.refers_str
        forma = f"📊 Ваша реферальная таблица: {value}"
    elif findex==97: # REF.user_refstat
        forma = f"🍕 *ВАША РЕФЕРАЛЬНАЯ ТАБЛИЦА* 👨‍👩‍👧‍👦 {value}"
    elif findex==98: # REF.user_refstat
        forma = f"🍕 ВАША РЕФЕРАЛЬНАЯ МАТРИЦА 📊 {value}"
    return forma


# NOTE: Inc_Day, Inc_Day_syn, and AUTODAY functions have been moved to cron_manager.py
# Import them from there if needed:
# from cron_manager import Inc_Day, Inc_Day_syn, AUTODAY


def Getask_day(day):
    """Get number of tasks for a given day."""
    mtask = 3
    print (f"Распорядок > день {day} по > {mtask} задачи")
    return mtask


def Get_Credos():
    """Get all game credits (Bales, Lives, Antes, Doles)."""
    Bales = get_credos(1)
    Lives = get_credos(2)
    Antes = get_credos(3)
    Doles = get_credos(4)
    return Bales, Lives, Antes, Doles


async def Inc_Lives(state: FSMContext, lives:int=1):
    """
    Increment user lives and notify.

    Args:
        state: FSMContext state object
        lives: Number of lives to add (can be negative)
    """
    if lives==0: return
    LIVES = get_credos(1)
    LIVES += lives  # начисление +1 ЖИЗНИ
    save_credos(1, LIVES)
    if lives>0: text = f"Приятный подарок\n✨ Зачислены жизни {lives} 💖"
    if lives<0: text = f"Нежданная новость\n👹 Сгорели жизни {lives} 💖"
    await SEX(text, state)

async def Inc_Vitas(state: FSMContext, vitas:int=1):
    """
    Increment user vitas and notify.

    Args:
        state: FSMContext state object
        vitas: Number of vitas to add
    """
    VITAS = get_credos(2)
    VITAS += vitas  # начисление +1 VITA
    save_credos(2, VITAS)
    text = f"Приятный подарок\n✨ Зачислена вита {vitas}"
    await SEX(text, state)

async def Inc_ref_Bales(referrer_id, add_bales, state: FSMContext):
    """
    Increment referrer bales (points) and notify.

    Args:
        referrer_id: Referrer user ID
        add_bales: Number of bales to add
        state: FSMContext state object
    """
    referrer_bales = Get_Ref_Bales(referrer_id)
    abalers = pluralize_ru(add_bales, "балл", "балла", "баллов")
    referrer_bales += add_bales # начисление +н БАЛЛ
    Update_Ref_Bales(referrer_id, referrer_bales)
    text = f"✨ Отличная новость ✨\nВам зачислены Баллы 🏆\nЗа выполнение ДЗ\nВыполненные пункты:\n"
# 1. История дня
    text += f"Всего получено: {abalers} 🏆"
    await SEX(text, state, SENDER=referrer_id)
    token = await Get_Var('BOT_TOKEN', state)
    # return Send_Stick(referrer_id, "веды судьба", token)


async def Inc_ref_Lives(referrer_id, add_lives, state: FSMContext):
    """
    Increment referrer lives and notify.

    Args:
        referrer_id: Referrer user ID
        add_lives: Number of lives to add
        state: FSMContext state object
    """
    referrer_lives = Get_Ref_Lives(referrer_id)
    alivers = pluralize_ru(add_lives, "жизнь", "жизни", "жизней")
    referrer_lives += add_lives # начисление +1 ЖИЗНИ
    Update_Ref_Lives(referrer_id, referrer_lives)
    text = f"✨Отличная новость✨\nВам зачислено +{alivers} 💖"
    await SEX(text, state, SENDER=referrer_id)
    token = await Get_Var('BOT_TOKEN', state)
    # return Send_Stick(referrer_id, "книга жизни", token)


async def Get_User_Day(state: FSMContext):
    """
    Get user's current day from state or database.

    Args:
        state: FSMContext state object

    Returns:
        int: Current day number
    """
    #user_data = state.get_data()
    # local_day = await Get_VAR('day', 1, state) # безопасное чтение
    # local_day = await Get_Var('day', state) # опасное чтение
    # print("GUD > Запрос дня с защитой: ", end='')
    # if local_day:
        # print("GUD > Считан локальный день: ", local_day)
        # return local_day
    # print ("GUD > Нет дня в памяти, ищем в базе юзера")
    server_day = get_day()
    if server_day:       # 1v БЕЗУПРЕЧНАЯ Серверная ИНКРА - защита от сменя дня
        print ("GUD > Загружаем день из базы")
        await Set_Var('day', server_day, state)
        return server_day
    else:
        print("GUD > Нету дня: Возвращаю => 1 день")
        return 1

async def Transcribe_audio(file_id: str, bot: Bot, state: FSMContext) -> str:
    """
    Transcribe audio file to text using Google Speech Recognition.

    Args:
        file_id: Telegram file ID of voice message
        bot: aiogram Bot instance
        state: FSMContext state object

    Returns:
        str: Transcribed text or error message
    """
# Получение файла голосового сообщения
    file = await bot.get_file(file_id)
    user_path = await Get_VAR('user_path', '.', state)
    user_nick = await Get_Var('user_nick', state)
    day = await Get_User_Day(state)
    daystring = "_day" + str(day)
    k = 1
    file_name  = user_nick + daystring + "_" + str(k) + ".ogg"
    ogg_file_path = os.path.join(user_path, file_name)
    while os.path.exists(ogg_file_path):
        k+=1
        file_name  = user_nick + daystring + "_" + str(k) + ".ogg"
        ogg_file_path = os.path.join(user_path, file_name)
# Скачивание файла
    await file.download_to_drive(ogg_file_path)
    try:
# Чтение и конвертация файла
        with open(ogg_file_path, 'rb') as f:
            voice_data = io.BytesIO(f.read())
        audio = AudioSegment.from_ogg(voice_data)
        audio_data = io.BytesIO()
        audio.export(audio_data, format="wav")
        audio_data.seek(0)
    except Exception as e:
        return f"err: Ошибка при конвертации аудио: {e}"
    with sr.AudioFile(audio_data) as source:
        recognizer = sr.Recognizer()
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language=LANG_CODE)
            return text
        except sr.UnknownValueError:
            return(f"err: Неизвестная ошибка распознавателя Google Speech Recognition")
        except sr.RequestError as e:
            return(f"err: Ошибка распознавателя Google Speech Recognition: {e}")


async def GetavaUser(user_id, user_nick, user_path, bot: Bot):
    """
    Get and download user avatar.

    Args:
        user_id: User ID
        user_nick: User nickname
        user_path: User path for saving avatar
        bot: aiogram Bot instance

    Returns:
        str: Path to avatar file or None
    """
# Получаем аватар пользователя
    # user_id = await Get_Uid(state)
    # user_nick = await Get_Var('user_nick', state)
    # user_path = await Get_Var('user_path', state)
    user_profile_photos = await bot.get_user_profile_photos(user_id)
    if user_profile_photos.total_count > 0:
        file_id = user_profile_photos.photos[0][-1].file_id  # Берем последнюю версию первой фотографии (наиболее качественную)
        user_file = await bot.get_file(file_id)
        ava_name = user_nick + ".jpg" # НОВ ФОРМАТ
        file_path = os.path.join(user_path, ava_name)
        #f"{user_path}/{ava_name}"
        if not os.path.isfile(file_path):
            print(f"Файл скачиваеца: {file_path}...", end='')
            await user_file.download_to_drive(file_path)
        print("Фото уже готово")
        return file_path
    else:
        print("У пользователя нет фотографии профиля")
        return None


async def Clear_user_TASKS(state: FSMContext):
    """
    Clear all user tasks (voice files and answer files).

    Args:
        state: FSMContext state object
    """
    user_id = await Get_Uid(state)     #
    user_path = await Get_Var('user_path', state)   # получаем юзер-папку
    print(f'Чистим все ответы юзера: {user_path}')
    for file_name in os.listdir(user_path):    # чистим от голосовых
        if file_name.endswith('.ogg'):
            file_path = os.path.join(user_path, file_name)
            os.remove(file_path)
            print(f'Файл голосовухи удален: {file_path}')
        if file_name.endswith('.json'):
            file_path = os.path.join(user_path, file_name)
            os.remove(file_path)
            print(f'Файл ответов удален: {file_path}')


# удаляем ответы
    await SEX("😢 Ваши все ответы были удалены 😉", state)
    await Adelay(1)
    Init_Answers(user_id)
    # await Set_Var('day', 0, state)  # сбрасываем день
    # await Inc_Day(state)  # теперь вызывает рестарт
