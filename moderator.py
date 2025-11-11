# MODERATOR 
import os, json, requests
from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from answers import Get_day_responses  #, Get_task_response
# from lifeman import save_status, get_status
from active import *
from passive import *
# from reports import *

bug_repo = {}
Moderator_DIR = 'LIFE-REPORTS' 
LIFE_CHAT_id = -1002232747079 # чат Жизнь
PAY_CHAT_id = -1002562493765 # чат Оплата
DEV_CHAT_id = PAY_CHAT_id
BUG = False
# -------------=------------------       

def is_BUG()->bool:
    return BUG

async def SEX_PRO(block_name, context: ContextTypes.DEFAULT_TYPE):
    Block_PAK = Make_Block(block_name)
    return await SEX_PROD(Block_PAK, context)
    
async def SEX_PROD(block_pak, context: ContextTypes.DEFAULT_TYPE):
    message_text, keyboard, picture_path = block_pak
    if picture_path:
        print ("SEX_PROD: Найдена фотка, отправляем фото-блок c меню")
        with open(picture_path, 'rb') as photo:
            return await SEX(message_text, context, DOC = photo, MENU = keyboard, FORMAT = 'B')
    else:
        print ("SEX_PROD: Фотка не найдена, отправляем текст c меню")
        return await SEX(message_text, context, MENU = keyboard, FORMAT = 'B')

async def Write_BUG(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BUG    
    Update_step(7, context)  # Write BUG-report    
    user_id = Get_Uid(context)
    user_name = Get_Var('user_nick', context)    
    t1 = Form_Port(16, None)  # шапка 1 длинная
    t2 = Form_Port(2, user_name)  # имя
    t3 = Form_Port(4, user_id) # айди
    t3 += "   >🔍>"
    header = "\n".join([t1, t2, t3])  
    MSG = await SEX(header, context, SENDER=DEV_CHAT_id)     
    Set_Var('rep_mid', MSG.message_id, context)
    # text = TextBlock('feed_bug')
    BUG = True
    await SEX_PRO('FEED_RUN', context)
    # button_1 = InlineKeyboardButton("Закончить ➡️", callback_data='☎️send')
    # button_2 = InlineKeyboardButton("Отмена", callback_data='☎️back')       
    # buttons = [[button_1, button_2]]
    # keybug = Make_KEYB(buttons)         
    # await SEX(text, context, MENU=keybug, FORMAT='B') 
    # return

async def Send_BUG(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BUG
    Update_step(19, context)  # exit mode
    BUG = False
    # await SEX("Ввод данных закончен 👌🏻\nВаши сообщения и файлы будут высланы на проверку 🙏", context)
    Moderator_ID = Get_Var ('MOD_ID', context)    
    print (">> Идет Извещение Модератора: BUG-report")
    # print(TEX)    
    
    rep_mid = Get_Var('rep_mid', context)
    chat_id = str(DEV_CHAT_id).replace('-100', '')
    message_link = f"https://t.me/c/{chat_id}/{rep_mid}"
    print('Репорт MSG LINK=', message_link)
    
    text = f"Уважаемый Модератор 🎅🏻\nВ наш DEV-чат пришел Рапорт об ошибке 🧾\n`{message_link}`" 
    
    
    await SEX(text, context, SENDER=Moderator_ID) 
    # await FEED_GOT(context)    
    await Adelay(0.5)
    # await bugInput_Forward (Moderator_ID, context)
    buttons = [[InlineKeyboardButton("На Страницу Статуса", callback_data='begin_game')]]
    text = "Ввод данных закончен 👌🏻\nВаши сообщения и файлы будут высланы на проверку 🙏"
    await Make_MENU(text, buttons, context) 
    return

  
 
async def MODER_RUN(choice, update, context: ContextTypes.DEFAULT_TYPE):
    TOKEN = Get_Var('BOT_TOKEN', context) 
    Moderator_ID = Get_Var ('MOD_ID', context)
    # status = get_status()
    
    
    if choice == '🎅🏻approve':
        print("> Модератор - ПРИНЯТЬ+ ")
        await Mod_Up_Approve(context)
    
    elif choice == '🎅🏻refuse':
        print("> Модератор - ОТКЛОНИТЬ- ")  
        # await SEX("Надо ввести причину отказа:", context, SENDER=Moderator_ID)
        await Mod_Up_Refuse(context)
    
    # elif choice == '🎅🏻back':
        # print("> Модератор переход в меню")  
        # await REP_Ready(rep_file, context)

async def Mod_Up_Approve(context: ContextTypes.DEFAULT_TYPE):
    TOKEN = Get_Var('BOT_TOKEN', context) 
    Moderator_ID = Get_Var ('MOD_ID', context)
    tarr = Get_Var ('user_tarif', context)
    print(f"Mod_Up_Approve 🎅  user_tarif {tarr}")
    Update_step(19, context)  # Silent Hill (Last Silence befor REPLICATOR)
    # lives = 1
    # if tarr==2:
        # lives = 3
    # if tarr==3:
        # lives = 10
    # lives = GET_BONS(tarr)
    price, vitas, lives = get_tariff_infoby_index(tarr)
    # поставили тариф платный в базу
    save_pays(tarr)        
    
    user_role = get_role()
    if not (IsUserPreme(user_role)):        
        user_role+='+'
        save_role(user_role)  
    # else:
        # return
    user_name = Get_Var ('user_nick', context)
    payd_text = 'Оплата одобрена ✅\nОткрыт доступ в платный раздел.\nА также начислены бонусные жизни и Вита'  
    payd_self = f'🧩 ОПЛАТА УСПЕШНА 🧩\n✅Игрок получает доступ в раздел "Профи" '
    await Inc_Lives(context, lives=lives)
    await Inc_Vitas(context, vitas=vitas)
    await SEX(payd_text, context)
    
    
    text = 'Менеджер ✅ Утвердил Оплату'
    prepay_text = Prep_MOC4(context) + '\n' + text
    text4 = Get_Var ('mid_Start_Text', context)+ '\n' + text 
    MSG = Get_Var ('mid_Start_Rules', context)
    if MSG:
        MSG3 = await SEX(text4, context, FORMAT='B', EDIT = MSG, SENDER=LIFE_CHAT_id) # СООБЩ в ЧАТ
    else:      
        MSG3 = await SEX(prepay_text, context, FORMAT='B', SENDER=LIFE_CHAT_id) # СООБЩ в ЧАТ
    
    
    
    await SEX(payd_self, context, SENDER = Moderator_ID )
    

    # Send_STICKER("крутой отчет", context)    #  Feed_Up_Approve     
    
async def Mod_Up_Refuse (context: ContextTypes.DEFAULT_TYPE):
    Moderator_ID = Get_Var ('MOD_ID', context)   
    Update_step(19, context)  # Silent Hill
    await SEX("Оплата ❌\nОТКЛОНЕНО🙅🏼МОДЕРАТОРОМ", context)
    await SEX("ОПЛАТА -❌- ОТКЛОНЕНО", context, SENDER=Moderator_ID)        

async def REP_DOWN(context: ContextTypes.DEFAULT_TYPE):
    text, keyb = Prep_MOC2(context)    
    return await SEMOD(text, keyb, context)

# async def REP_Refuse(context: ContextTypes.DEFAULT_TYPE):
    # text = "ОПЛАТА -❌- ОТКЛОНЕНО🙅🏼МОДЕРАТОРОМ"
    # await SEX(text, context)
    # text, keyb = Prep_MOC3(context) 
    # Update_step(8, context)    
    # return await Mod_Up_Refuse(text, context)
    
    
async def SEMOD(message, keyboard, context: ContextTypes.DEFAULT_TYPE):
    Moderator_ID = Get_Var ('MOD_ID', context)
    Moderator_Name = Get_Var ('MOD_NAME', context)
    print(f"ПОСЛАНИЕ ДЛЯ МОДЕРАТОРА 🎅🏻 {Moderator_Name}")
    return await SEX(message, context, SENDER=Moderator_ID, MENU=keyboard, FORMAT='B')
    # context.bot.send_message(chat_id=Moderator_ID, text=message, reply_markup=keyboard)       


def Prep_MOC4(context: ContextTypes.DEFAULT_TYPE):
    text = Form_Port(26, None)       # шапка 6м
    name = Get_Var ('user_nick', context)
    name2 = Get_Var ('user_name', context)
    uid = Get_Uid(context)
    # day = Get_Var('day', context)    
    text += f"\n👩🏻 Псевдоним: {ESU(name)}➖{ESU(name2)}\n🆔 ID игрока: {uid}"
    # keybuts = [[InlineKeyboardButton("👌🏻 ПРИНЯТЬ +💖", callback_data='☎️approve'),
        # InlineKeyboardButton("🙅🏼 ОТКЛОНИТЬ", callback_data='☎️refuse')]]     
    # keyboard = Make_KEYB(keybuts)  
    return text 
    
    
def Prep_MOC5(mess:str, context: ContextTypes.DEFAULT_TYPE):
    
    # text = Form_Port(26, None)       # шапка 6м
    name = Get_Var ('user_nick', context)
    # name2 = Get_Var ('user_name', context)
    # uid = Get_Uid(context)
    # day = Get_Var('day', context)     \n📅 ДЕНЬ: {day
    # f"\n👩🏻 Псевдоним: {ESU(name)} aka {ESU(name2)}\n🆔 ID юзера: {uid}"
    text = Prep_MOC4(context)
    text += f'\n 🧾 *Запись добавлена в журнал* [{name} ▶️ ОПЛАТА]({mess})'
    keybuts = [[InlineKeyboardButton("ОДОБРИТЬ👌🏻ОПЛАТУ", callback_data='🎅🏻approve'),
        InlineKeyboardButton("ОТКЛОНИТЬ🙅🏼ОПЛАТУ", callback_data='🎅🏻refuse')]]     
    keyboard = Make_KEYB(keybuts)  
    return text, keyboard     
        
# async def BugSpy_Handler_Old(msg:str, context: ContextTypes.DEFAULT_TYPE):
    # user_name = Get_Var ('user_nick', context)
    # user_id = Get_Uid(context)
    # t1 = Form_Port(16, None)       # шапка 3м1
    # t2 = Form_Port(2, user_name) # имя
    # t3 = Form_Port(4, user_id) #     
    # text = "\n".join([t1, t2, t3, msg])
    # await context.bot.send_message(chat_id=LIFE_CHAT_id, text=text)    
       
# async def bugInput_Handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user_id = Get_Uid(context)   
    # if user_id not in bug_repo:
        # bug_repo[user_id] = {"text": [], "files": [], "photos": []}    
    # if update.message.text:
        # bug_repo[user_id]["text"].append(update.message.text)
        # print("-Добавлен текст в багреп-")
    # elif update.message.document:
        # file = await update.message.document.get_file()
        # bug_repo[user_id]["files"].append(file)
        # print("-Добавлен док в багреп-")
    # elif update.message.photo:
        # photo = update.message.photo[-1]  # Берем самое большое изображение
        # file = await photo.get_file()
        # bug_repo[user_id]["photos"].append(file)
        # print("-Добавлено фото в багреп-")
        
# async def bugInput_Forward(chat_id, context: ContextTypes.DEFAULT_TYPE):
    # bot = context.bot
    # user_id = Get_Uid(context)     
    # TEX = ">> ИДЕТ ОТПРАВКА БАГ-РЕПОРТА админу: " 
    # print(TEX)
    # text = "Уважаемый Модератор 💡\nТут отчет об ошибке 🧾 в нашей игре 'Книга Жизни'"
    # await SEI(text, chat_id, context)   
    # if user_id in bug_repo:
        # for text in bug_repo[user_id]["text"]:
            # await bot.send_message(chat_id=chat_id, text=text) 
            # print(f"> отправлен блок 'text' в чат: {chat_id}")        
        # for file in bug_repo[user_id]["files"]: 
            # await bot.send_document(chat_id=chat_id, document=file.file_id)
            # print(f"> отправлен блок 'document' в чат: {chat_id}")        
        # for photo in bug_repo[user_id]["photos"]:
            # await bot.send_photo(chat_id=chat_id, photo=photo.file_id)
            # print(f"> отправлено фото в чат: {chat_id}")        
        # bug_repo[user_id] = {"text": [], "files": [], "photos": []}  # очищаем данные
    # else:
        # await SEI("Нет данных для пересылки", chat_id, context) 
    # await FEED_GOT(context)   