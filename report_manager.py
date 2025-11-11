# report_manager.py
"""
Генерация и отправка отчётов: дневных, недельных, финальных.
"""

import os
import json
from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from const import QUESTIONS, MODERATOR_DIR, LIFE_CHAT_ID, PAY_CHAT_ID, DEV_CHAT_ID, NUM_TASKS_PER_DAY, MAX_DAYS
from utils import ESU, CYFER, Get_Uid, Get_Var, Set_Var, Adelay
from ui_blocks import SEX, Make_KEYB, Make_MENU, SEX_PRO # Assuming SEX, Make_KEYB, Make_MENU, SEX_PRO are in ui_blocks.py
from lifeman_new import get_day, get_role, get_pays, save_pays, save_role, get_credos, save_credos, IsUserPreme # Import from lifeman_new.py

# Global variable for bug reporting status
BUG = False

def is_BUG()->bool:
    return BUG

# Bug reporting repository
bug_repo = {}

# Message formatting functions from active.py
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

# Bug reporting functions from moderator.py
async def Write_BUG(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BUG    
    # Update_step(7, context)  # Write BUG-report - assuming Update_step is in utils.py
    user_id = Get_Uid(context) # Assuming Get_Uid is in utils.py
    user_name = Get_Var('user_nick', context) # Assuming Get_Var is in utils.py
    t1 = Form_Port(16, None)  # шапка 1 длинная
    t2 = Form_Port(2, user_name)  # имя
    t3 = Form_Port(4, user_id) # айди
    t3 += "   >🔍>"
    header = "\n".join([t1, t2, t3])  
    MSG = await SEX(header, context, SENDER=DEV_CHAT_ID) # Assuming DEV_CHAT_ID is in const.py and SEX in ui_blocks.py
    Set_Var('rep_mid', MSG.message_id, context) # Assuming Set_Var is in utils.py
    BUG = True
    await SEX_PRO('FEED_RUN', context) # Assuming SEX_PRO is in ui_blocks.py

async def Send_BUG(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BUG
    # Update_step(19, context)  # exit mode - assuming Update_step is in utils.py
    BUG = False
    Moderator_ID = Get_Var ('MOD_ID', context) # Assuming MOD_ID is stored in user_data
    print (">> Идет Извещение Модератора: BUG-report")
    
    rep_mid = Get_Var('rep_mid', context)
    chat_id = str(DEV_CHAT_ID).replace('-100', '') # Assuming DEV_CHAT_ID is in const.py
    message_link = f"https://t.me/c/{chat_id}/{rep_mid}"
    print('Репорт MSG LINK=', message_link)
    
    text = f"Уважаемый Модератор 🎅🏻\nВ наш DEV-чат пришел Рапорт об ошибке 🧾\n`{message_link}`" 
    
    await SEX(text, context, SENDER=Moderator_ID) # Assuming SEX in ui_blocks.py
    await Adelay(0.5) # Assuming Adelay in utils.py
    buttons = [[InlineKeyboardButton("На Страницу Статуса", callback_data='begin_game')]]
    text = "Ввод данных закончен 👌🏻\nВаши сообщения и файлы будут высланы на проверку 🙏"
    await Make_MENU(text, buttons, context) # Assuming Make_MENU in ui_blocks.py

def Prep_MOC4(context: ContextTypes.DEFAULT_TYPE):
    text = Form_Port(26, None)       # шапка 6м
    name = Get_Var ('user_nick', context)
    name2 = Get_Var ('user_name', context)
    uid = Get_Uid(context)
    text += f"\n👩🏻 Псевдоним: {ESU(name)}➖{ESU(name2)}\n🆔 ID игрока: {uid}"
    return text 
    
def Prep_MOC5(mess:str, context: ContextTypes.DEFAULT_TYPE):
    name = Get_Var ('user_nick', context)
    text = Prep_MOC4(context)
    text += f'\n 🧾 *Запись добавлена в журнал* [{name} ▶️ ОПЛАТА]({mess})'
    keybuts = [[InlineKeyboardButton("ОДОБРИТЬ👌🏻ОПЛАТУ", callback_data='🎅🏻approve'),
        InlineKeyboardButton("ОТКЛОНИТЬ🙅🏼ОПЛАТУ", callback_data='🎅🏻refuse')]]     
    keyboard = Make_KEYB(keybuts) # Make_KEYB(keybuts) # Assuming Make_KEYB in ui_blocks.py
    return text, keyboard     

# User answers management functions from answers.py
# numtask = 3 # From answers.py, should be NUM_TASKS_PER_DAY from const.py
# maxdays = 28 # From answers.py, should be MAX_DAYS from const.py

def get_LAB_file(q_num: int, user_id:int, user_path: str) -> str:
    labook_file = f"USERLAB-{user_id}-Q{q_num}.json"
    file_path = os.path.join(user_path, labook_file)
    return file_path

def Init_Answers(user_id: int, user_path: str):
    print(" > Init_Answers > Форматируем ОТВЕТЫ")
    tasks = [QUESTIONS[i] for i in range(1, NUM_TASKS_PER_DAY + 1)] # Use QUESTIONS from const.py
    for task_index in range(1, NUM_TASKS_PER_DAY + 1):
        file_path = get_LAB_file(task_index, user_id, user_path)
        zero = {"": tasks[task_index-1]}
        Set_user_red(zero, task_index, user_id, user_path)

def Get_user_re(q_num: int, user_id: int, user_path: str):
    try:
        file_path = get_LAB_file(q_num, user_id, user_path)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error reading user responses: {e}")
        return None

def Get_all_responses(user_id: int, user_path: str):
    block_respo = []
    for task_index in range(1, NUM_TASKS_PER_DAY + 1):
        file_path = get_LAB_file(task_index, user_id, user_path)
        if os.path.exists(file_path):
            responses = Get_user_re(task_index, user_id, user_path)
            if responses:
                responsess = str(responses)
                block_respo.append(responsess)
    all_responses = '\n'.join(block_respo)
    return all_responses

def Set_user_red(responses, q_num: int, user_id: int, user_path: str, day: str = None):
    try:
        file_path = get_LAB_file(q_num, user_id, user_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        existing_data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, dict):
                        existing_data = {}
                except json.JSONDecodeError:
                    existing_data = {}
        if day is not None:
            existing_data[day] = responses
        else:
            existing_data.update(responses)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении ответа: {e}")
        return False

def Get_day_responses(day, user_id: int, user_path: str):
    day_respo = []
    for task_index in range(1, NUM_TASKS_PER_DAY + 1):
        file_path = get_LAB_file(task_index, user_id, user_path)
        if os.path.exists(file_path):
            responses = Get_user_re(task_index, user_id, user_path)
            if responses:
                response = responses.get(str(day))
                day_respo.append(response)
    return day_respo

def Get_task_response(task_index, day, user_id: int, user_path: str):
    task_index += 1
    file_path = get_LAB_file(task_index, user_id, user_path)
    if os.path.exists(file_path):
        responses = Get_user_re(task_index, user_id, user_path)
        if responses:
            return responses.get(str(day))
    return None

def Update_task_response(task_index, day, response_text, user_id: int, user_path: str):
    day = str(day) if day else "1"
    task_index += 1
    print(f"Update_task_response ПРИШЛО ~ Tindex->{task_index}  День->{day}")
    try:
        ok = Set_user_red(response_text, task_index, user_id, user_path, day=day)
        if ok:
            print(f"Ответ для задачи {task_index} день {day} обновлен: {response_text}")
            return True
        else:
            print(f"Ошибка в Set_user_red {task_index} день {day} обновлен: {response_text}")
            return False
    except Exception as e:
        print(f"Ошибка при обновлении ответа: {str(e)}")
        return False

def delete_user_responses(user_id: int, user_path: str):
    Init_Answers(user_id, user_path)

# Moderator report preparation functions from moderator.py
def Prep_MOC4(context: ContextTypes.DEFAULT_TYPE):
    text = Form_Port(26, None)       # шапка 6м
    name = Get_Var ('user_nick', context)
    name2 = Get_Var ('user_name', context)
    uid = Get_Uid(context)
    text += f"\n👩🏻 Псевдоним: {ESU(name)}➖{ESU(name2)}\n🆔 ID игрока: {uid}"
    return text 
    
def Prep_MOC5(mess:str, context: ContextTypes.DEFAULT_TYPE):
    name = Get_Var ('user_nick', context)
    text = Prep_MOC4(context)
    text += f'\n 🧾 *Запись добавлена в журнал* [{name} ▶️ ОПЛАТА]({mess})'
    keybuts = [[InlineKeyboardButton("ОДОБРИТЬ👌🏻ОПЛАТУ", callback_data='🎅🏻approve'),
        InlineKeyboardButton("ОТКЛОНИТЬ🙅🏼ОПЛАТУ", callback_data='🎅🏻refuse')]]     
    keyboard = Make_KEYB(keybuts)
    return text, keyboard
    
# Report generation functions
def format_daily_report(context) -> str:
    day = get_day(Get_Uid(context)) # Use get_day from lifeman_new
    user_id = Get_Uid(context)
    user_path = Get_Var('user_path', context) # Assuming user_path is stored in context
    responses = Get_day_responses(day, user_id, user_path)
    name = Get_Var('user_nick', context)

    report = f"📓 *Отчёт за день {day} — {name}*\n\n"
    for i, question_text in enumerate(QUESTIONS.values()): # Use QUESTIONS from const.py
        answer = responses[i] if i < len(responses) else None
        status = "✅" if answer else "❌"
        report += f"{status} **{question_text}**\n"
        if answer:
            report += f"`{answer}`\n"
        report += "\n"
    return report

async def generate_and_send_report(context, final: bool = False):
    if final:
        # TODO: вызов freya_final + генерация PDF/HTML
        text = "🏆 *ФИНАЛЬНЫЙ ОТЧЁТ МАРАФОНА*\n\nСкоро будет доступен полный разбор от FREYA."
    else:
        text = format_daily_report(context)

    # Отправляем по частям, если длинный
    if len(text) > 4000:
        # await ASPLITTER(text, context) # ASPLITTER needs to be moved or reimplemented
        await SEX(text, context, FORMAT="B") # For now, send as one message
    else:
        await SEX(text, context, FORMAT="B") # parse_mode="Markdown" is handled by FORMAT='B'
