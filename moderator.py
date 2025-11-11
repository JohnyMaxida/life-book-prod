# MODERATOR
"""
Moderator functions for Life-Book bot.
Migrated to aiogram 3.x.
"""
import os, json, requests
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from report_manager import Get_day_responses  # Moved from answers.py to report_manager.py
# Import specific functions instead of wildcard imports
from active import (Form_Port, Inc_Lives, Inc_Vitas, get_tariff_infoby_index)
from passive import (Make_Block, Get_Var, Set_Var, Get_Uid, Update_step, Adelay, ESU)
from ui_blocks import SEX, Make_KEYB, Make_MENU
from lifeman_new import get_role, save_pays, save_role, IsUserPreme

bug_repo = {}
Moderator_DIR = 'LIFE-REPORTS' 
LIFE_CHAT_id = -1002232747079 # чат Жизнь
PAY_CHAT_id = -1002562493765 # чат Оплата
DEV_CHAT_id = PAY_CHAT_id
BUG = False
# -------------=------------------       

def is_BUG()->bool:
    return BUG

async def SEX_PRO(block_name: str, state: FSMContext):
    """Send block with picture if available."""
    Block_PAK = Make_Block(block_name)
    return await SEX_PROD(Block_PAK, state)

async def SEX_PROD(block_pak, state: FSMContext):
    """Send block with picture or text menu."""
    message_text, keyboard, picture_path = block_pak
    if picture_path:
        print ("SEX_PROD: Найдена фотка, отправляем фото-блок c меню")
        with open(picture_path, 'rb') as photo:
            return await SEX(message_text, state, DOC = photo, MENU = keyboard, FORMAT = 'B')
    else:
        print ("SEX_PROD: Фотка не найдена, отправляем текст c меню")
        return await SEX(message_text, state, MENU = keyboard, FORMAT = 'B')

async def Write_BUG(state: FSMContext):
    """
    Write bug report to DEV chat.

    Args:
        state: FSMContext for user state management
    """
    global BUG
    await Update_step(7, state)  # Write BUG-report
    user_id = await Get_Uid(state)
    user_name = await Get_Var('user_nick', state)
    t1 = Form_Port(16, None)  # шапка 1 длинная
    t2 = Form_Port(2, user_name)  # имя
    t3 = Form_Port(4, user_id) # айди
    t3 += "   >🔍>"
    header = "\n".join([t1, t2, t3])
    MSG = await SEX(header, state, SENDER=DEV_CHAT_id)
    await Set_Var('rep_mid', MSG.message_id, state)
    BUG = True
    await SEX_PRO('FEED_RUN', state)

async def Send_BUG(state: FSMContext):
    """
    Send bug report notification to moderator.

    Args:
        state: FSMContext for user state management
    """
    global BUG
    await Update_step(19, state)  # exit mode
    BUG = False
    Moderator_ID = await Get_Var('MOD_ID', state)
    print (">> Идет Извещение Модератора: BUG-report")

    rep_mid = await Get_Var('rep_mid', state)
    chat_id = str(DEV_CHAT_id).replace('-100', '')
    message_link = f"https://t.me/c/{chat_id}/{rep_mid}"
    print('Репорт MSG LINK=', message_link)

    text = f"Уважаемый Модератор 🎅🏻\nВ наш DEV-чат пришел Рапорт об ошибке 🧾\n`{message_link}`"

    await SEX(text, state, SENDER=Moderator_ID)
    await Adelay(0.5)
    buttons = [[InlineKeyboardButton(text="На Страницу Статуса", callback_data='begin_game')]]
    text = "Ввод данных закончен 👌🏻\nВаши сообщения и файлы будут высланы на проверку 🙏"
    await Make_MENU(text, buttons, state)
    return

  
 
async def MODER_RUN(choice: str, state: FSMContext):
    """
    Handle moderator actions.

    Args:
        choice: Moderator's choice (approve/refuse)
        state: FSMContext for user state management
    """
    TOKEN = await Get_Var('BOT_TOKEN', state)
    Moderator_ID = await Get_Var('MOD_ID', state)

    if choice == '🎅🏻approve':
        print("> Модератор - ПРИНЯТЬ+ ")
        await Mod_Up_Approve(state)

    elif choice == '🎅🏻refuse':
        print("> Модератор - ОТКЛОНИТЬ- ")
        await Mod_Up_Refuse(state)

async def Mod_Up_Approve(state: FSMContext):
    """
    Approve payment and grant user premium access.

    Args:
        state: FSMContext for user state management
    """
    TOKEN = await Get_Var('BOT_TOKEN', state)
    Moderator_ID = await Get_Var('MOD_ID', state)
    tarr = await Get_Var('user_tarif', state)
    print(f"Mod_Up_Approve 🎅  user_tarif {tarr}")
    await Update_step(19, state)  # Silent Hill (Last Silence befor REPLICATOR)

    price, vitas, lives = get_tariff_infoby_index(tarr)
    # поставили тариф платный в базу
    save_pays(tarr)

    user_role = get_role()
    if not (IsUserPreme(user_role)):
        user_role+='+'
        save_role(user_role)

    user_name = await Get_Var('user_nick', state)
    payd_text = 'Оплата одобрена ✅\nОткрыт доступ в платный раздел.\nА также начислены бонусные жизни и Вита'
    payd_self = f'🧩 ОПЛАТА УСПЕШНА 🧩\n✅Игрок получает доступ в раздел "Профи" '
    await Inc_Lives(state, lives=lives)
    await Inc_Vitas(state, vitas=vitas)
    await SEX(payd_text, state)

    text = 'Менеджер ✅ Утвердил Оплату'
    prepay_text = await Prep_MOC4(state) + '\n' + text
    text4 = await Get_Var('mid_Start_Text', state) + '\n' + text
    MSG = await Get_Var('mid_Start_Rules', state)
    if MSG:
        MSG3 = await SEX(text4, state, FORMAT='B', EDIT = MSG, SENDER=LIFE_CHAT_id) # СООБЩ в ЧАТ
    else:
        MSG3 = await SEX(prepay_text, state, FORMAT='B', SENDER=LIFE_CHAT_id) # СООБЩ в ЧАТ

    await SEX(payd_self, state, SENDER = Moderator_ID )

async def Mod_Up_Refuse(state: FSMContext):
    """
    Refuse payment.

    Args:
        state: FSMContext for user state management
    """
    Moderator_ID = await Get_Var('MOD_ID', state)
    await Update_step(19, state)  # Silent Hill
    await SEX("Оплата ❌\nОТКЛОНЕНО🙅🏼МОДЕРАТОРОМ", state)
    await SEX("ОПЛАТА -❌- ОТКЛОНЕНО", state, SENDER=Moderator_ID)

async def REP_DOWN(state: FSMContext):
    """Prepare and send moderator report."""
    text, keyb = await Prep_MOC2(state)
    return await SEMOD(text, keyb, state)

# async def REP_Refuse(context: ContextTypes.DEFAULT_TYPE):
    # text = "ОПЛАТА -❌- ОТКЛОНЕНО🙅🏼МОДЕРАТОРОМ"
    # await SEX(text, context)
    # text, keyb = Prep_MOC3(context) 
    # Update_step(8, context)    
    # return await Mod_Up_Refuse(text, context)
    
    
async def SEMOD(message: str, keyboard, state: FSMContext):
    """
    Send message to moderator.

    Args:
        message: Message text
        keyboard: Keyboard markup
        state: FSMContext for user state management
    """
    Moderator_ID = await Get_Var('MOD_ID', state)
    Moderator_Name = await Get_Var('MOD_NAME', state)
    print(f"ПОСЛАНИЕ ДЛЯ МОДЕРАТОРА 🎅🏻 {Moderator_Name}")
    return await SEX(message, state, SENDER=Moderator_ID, MENU=keyboard, FORMAT='B')

async def Prep_MOC4(state: FSMContext):
    """Prepare moderator console text (payment header)."""
    text = Form_Port(26, None)       # шапка 6м
    name = await Get_Var('user_nick', state)
    name2 = await Get_Var('user_name', state)
    uid = await Get_Uid(state)
    text += f"\n👩🏻 Псевдоним: {ESU(name)}➖{ESU(name2)}\n🆔 ID игрока: {uid}"
    return text

async def Prep_MOC5(mess: str, state: FSMContext):
    """Prepare moderator console with payment approval buttons."""
    name = await Get_Var('user_nick', state)
    text = await Prep_MOC4(state)
    text += f'\n 🧾 *Запись добавлена в журнал* [{name} ▶️ ОПЛАТА]({mess})'
    keybuts = [[InlineKeyboardButton(text="ОДОБРИТЬ👌🏻ОПЛАТУ", callback_data='🎅🏻approve'),
        InlineKeyboardButton(text="ОТКЛОНИТЬ🙅🏼ОПЛАТУ", callback_data='🎅🏻refuse')]]
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