# ACTIVE
import os, io, requests
from datetime import datetime #, timedelta #, time
from pydub import AudioSegment
import speech_recognition as sr
#from telegram import Update
from telegram.ext import ContextTypes
from passive import *
from lifeman import *
from answers import Update_task_response, Get_task_response, Init_Answers
from temporal import Show_Game_Time, S2TIME, pluralize_ru, Adelay
# status_smiles = ['❌','🙋🏼','👌🏻','🙅🏼','✅']
MAX_DAYS = 28
LANG_CODE = "ru-RU"
Start_Time:datetime = None

def Ext_SS(stat_string):
    smile = stat_string[0]
    return smile+"\n"+stat_string
    
def Ext_SSS(stat_string, SYM):
    smile = stat_string[0]
    return smile+"\n"+SYM+stat_string+SYM     

def Ext_BS(stat_string):
    return Ext_SSS(stat_string, '*')
    
def Ext_CS(stat_string):
    return Ext_SSS(stat_string, '_') 

def Ext_TS(stat_string):
    return Ext_SSS(stat_string, '`')   
    
def Form_Port(findex, value) -> str:
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

async def Inc_Day(context: ContextTypes.DEFAULT_TYPE):
    # Send_STICKER("кот монах", context)
    text = Inc_Day_syn(context)
    return await SEX(text, context)

def Inc_Day_syn(context: ContextTypes.DEFAULT_TYPE):
    # new_day = Get_Var('day', context) + 1
    new_day = Get_User_Day(context) + 1
    if new_day >= MAX_DAYS:
        print("Охренеть, дней больше чем массив! Начинаем сначала.")
        new_day = 1
    print(f">INC> Новый день: {new_day}")
    Set_Var('day', new_day, context)        
    save_day(new_day)
    # save_status(0) # статус дня сбрасывается
    text = f"Ура 🌟 Поздравляю Вас с началом Нового дня {new_day} 😊\n✳️ Сделайте растарт бота по команде /start"
    return text


def AUTODAY(context: ContextTypes.DEFAULT_TYPE):
    days_pass = Get_Var('day_pass', context)
    if days_pass:
        Set_Var('day', days_pass - 1, context)        
        Inc_Day_syn(context) 
    return days_pass


def Getask_day(day):
    mtask = 3
    print (f"Распорядок > день {day} по > {mtask} задачи")
    return mtask       
    
# def Is_holiday(day:int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    # global Start_Time
    # return day in [7, 14, 21, 28] 
    # if Start_Time is None:        
        # user_stime = Get_Var('user_stime', context)
        # if isinstance(user_stime, datetime):
            # Start_Time = user_stime
        # else:
            # Start_Time  = S2TIME(user_stime)        
    # return Is_day_sunday(day, Start_Time)
     
# def CARDofDay(day:int, context: ContextTypes.DEFAULT_TYPE):
    # shift = 0
    # for k in range(1, day+1):
        # if Is_holiday(k, context):
            # shift += 1
    # card = day - shift
    # return card
    
       
       
def Get_Credos():
    Bales = get_credos(1)
    Lives = get_credos(2)
    Antes = get_credos(3)
    Doles = get_credos(4)
    return Bales, Lives, Antes, Doles 

# async def Inc_Bales(context: ContextTypes.DEFAULT_TYPE):
    # BALES = get_credos(1) # OBSO
    # BALES += 1  # начисление +1 Балла
    # save_credos(1, BALES)
    # text = "Приятная новость -✨- Вам зачислен +1 🏆 БАЛЛ"    
    # await SEX (text, context)
    # Send_STICKER("мир заботица", context)    # мир заботица      


    
async def Inc_Lives(context: ContextTypes.DEFAULT_TYPE, lives:int=1):
    if lives==0: return
    LIVES = get_credos(1)
    LIVES += lives  # начисление +1 ЖИЗНИ
    save_credos(1, LIVES)
    if lives>0: text = f"Приятный подарок\n✨ Зачислены жизни {lives} 💖" 
    if lives<0: text = f"Нежданная новость\n👹 Сгорели жизни {lives} 💖"     
    await SEX(text, context)
    
async def Inc_Vitas(context: ContextTypes.DEFAULT_TYPE, vitas:int=1):
    VITAS = get_credos(2)
    VITAS += vitas  # начисление +1 ЖИЗНИ
    save_credos(2, VITAS)
    text = f"Приятный подарок\n✨ Зачислена вита {vitas}"    
    await SEX(text, context)    
    
async def Inc_ref_Bales(referrer_id, add_bales, context: ContextTypes.DEFAULT_TYPE):
    referrer_bales = Get_Ref_Bales(referrer_id)
    abalers = pluralize_ru(add_bales, "балл", "балла", "баллов")
    referrer_bales += add_bales # начисление +н БАЛЛ
    Update_Ref_Bales(referrer_id, referrer_bales) 
    text = f"✨ Отличная новость ✨\nВам зачислены Баллы 🏆\nЗа выполнение ДЗ\nВыполненные пункты:\n"
# 1. История дня
    text += f"Всего получено: {abalers} 🏆" 
    await SEX(text, context, SENDER=referrer_id) 
    token = Get_Var('BOT_TOKEN', context)
    # return Send_Stick(referrer_id, "веды судьба", token)    
    
    
async def Inc_ref_Lives(referrer_id, add_lives, context: ContextTypes.DEFAULT_TYPE):
    referrer_lives = Get_Ref_Lives(referrer_id)
    alivers = pluralize_ru(add_lives, "жизнь", "жизни", "жизней")
    referrer_lives += add_lives # начисление +1 ЖИЗНИ
    Update_Ref_Lives(referrer_id, referrer_lives) 
    text = f"✨Отличная новость✨\nВам зачислено +{alivers} 💖"
    await SEX(text, context, SENDER=referrer_id)
    token = Get_Var('BOT_TOKEN', context)
    # return Send_Stick(referrer_id, "книга жизни", token)



















def Get_User_Day(context: ContextTypes.DEFAULT_TYPE):
    #user_data = context.user_data
    # local_day = Get_VAR('day', 1, context) # безопасное чтение
    # local_day = Get_Var('day', context) # опасное чтение
    # print("GUD > Запрос дня с защитой: ", end='')
    # if local_day:
        # print("GUD > Считан локальный день: ", local_day)
        # return local_day   
    # print ("GUD > Нет дня в памяти, ищем в базе юзера")
    server_day = get_day()
    if server_day:       # 1v БЕЗУПРЕЧНАЯ Серверная ИНКРА - защита от сменя дня
        print ("GUD > Загружаем день из базы")
        Set_Var('day', server_day, context)
        return server_day  
    else:
        print("GUD > Нету дня: Возвращаю => 1 день")
        return 1
 
async def Transcribe_audio(file_id: str, context: ContextTypes.DEFAULT_TYPE) -> str:
# Получение файла голосового сообщения
    file = await context.bot.get_file(file_id)
    user_path = Get_VAR ('user_path', '.', context)
    user_nick = Get_Var ('user_nick', context)
    day = Get_User_Day(context)
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

    ava_name = user_nick + ".jpg" # НОВ ФОРМАТ
    file_path = os.path.join(user_path, ava_name)

async def GetavaUser(user_id, user_nick, user_path, context: ContextTypes.DEFAULT_TYPE):
# Получаем аватар пользователя
    # user_id = Get_Uid(context)      
    # user_nick = Get_Var('user_nick', context)
    # user_path = Get_Var('user_path', context) 
    user_profile_photos = await context.bot.get_user_profile_photos(user_id)    
    if user_profile_photos.total_count > 0:
        file_id = user_profile_photos.photos[0][-1].file_id  # Берем последнюю версию первой фотографии (наиболее качественную)
        user_file = await context.bot.get_file(file_id)        
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


        
async def Clear_user_TASKS(context: ContextTypes.DEFAULT_TYPE):
    user_id = Get_Uid(context)     #  
    user_path = Get_Var('user_path', context)   # получаем юзер-папку
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
    await SEX("😢 Ваши все ответы были удалены 😉", context)
    await Adelay(1)
    Init_Answers(user_id)
    # Set_Var('day', 0, context)  # сбрасываем день
    # await Inc_Day(context)  # теперь вызывает рестарт

