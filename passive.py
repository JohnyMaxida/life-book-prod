# PASSIVE
LANG = 'ru'
import sys, os, json, requests
import mimetypes
from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from temporal import Adelay, Show_Game_Time, get_utc_string
from lifeman import save_timezone, get_role, get_pays, Get_DONNA_URL, Get_UNI_URL, Get_AXI0M_REF, Get_AXI5M_URL
from utils import Generate_Ref_Code, BOGDAN_URL, DONNA_URL, UNILIV_URL, AXIOM5_URL, AXIOM_REF, AXIOM_URL
from utils import Get_Uid, Get_Var, Get_VAR, Set_Var, Update_step, UMR, ESC
from ui_blocks import SEX, SEFoB, SEFoM, Make_MENU, Make_MENB, Make_KEYB
from lifeBlock import LIFE_BLOCK

TARIFS = {
    5: {"vita": 50, "life": 2},
    10: {"vita": 100, "life": 5},
    20: {"vita": 200, "life": 11},
    50: {"vita": 500, "life": 25},
    100: {"vita": 1000, "life": 55},
    200: {"vita": 2000, "life": 125},
    500: {"vita": 5000, "life": 265},
    1000: {"vita": 10000, "life": 599}
}

# LIFE_BOOK = None
# LIFE_BLOCK = None
BOT_NAME = None 
ART_DIR = None
ARTBLOK_DIR = None

class TEXTBLOCK:
    def __init__(self, item_id, title, text, picture, menu):
        self.id = item_id
        self.title = title
        self.text = text
        self.picture = picture
        self.menu = menu

    def display(self):
        print(f"ID: {self.id}")
        print(f"Title: {self.title}")
        print(f"Picture: {self.picture}")
        print(f"Menu: {self.menu}")
        print(f"Message: {self.text}")


def get_tariff_info(usdt_amount):
    sorted_keys = sorted(TARIFS.keys())
    
    if usdt_amount not in TARIFS:
        return None, None, None  # Если такого тарифа нет
    
    index = sorted_keys.index(usdt_amount)
    vita = TARIFS[usdt_amount]["vita"]
    lifes = TARIFS[usdt_amount]["life"]
    
    return index, vita, lifes
    
    
# Получить Vita и Hearts по индексу тарифа
def get_tariff_infoby_index(index):
    sorted_keys = sorted(TARIFS.keys())
    if 0 <= index < len(sorted_keys):
        usdt_key = sorted_keys[index]
        vita = TARIFS[usdt_key]["vita"]
        life = TARIFS[usdt_key]["life"]
        return usdt_key, vita, life  # Возвращаем USDT, Vita, Life
    else:
        return None, None, None  # Неверный индекс  
    
    
# Проверяем для 100 USDT
# usdt = 100
# index, vita, hearts = get_tariff_info(usdt)

# if index is not None:
    # print(f"Тариф {usdt} USDT:")
    # print(f"  Индекс: {index}")
    # print(f"  Vita: {vita}")
    # print(f"  Hearts: {hearts}♥️")
# else:
    # print(f"Тариф для {usdt} USDT не найден.")



def IsPREM():
    return get_pays() 
 
def IsUserPREM() -> bool:
    prem = IsPREM()
    return prem>0 
 
def IsUserPreme(role:str=None) -> bool:
    if role is None:
        role = get_role()
    return ('+' in role)
    
 
def Make_Block(block_name):
    print("Make_Block > ", block_name)
    Block = Get_Block(block_name)
    # print(" > ", Block.title)
    if Block is None:
        return f"> Error find a block: {ESU(block_name)}", None, None
    # print("Text > ", Block.text.split('\n')[0])
    
    # Проверяем наличие картинки
    picture_path = None
    if Block.picture:
        picture_path = f"{Block.picture}.jpg"
        pic_file = os.path.join(ARTBLOK_DIR, picture_path)
        picture_path = pic_file if os.path.isfile(pic_file) else None
    print("Picture > ", picture_path)

    # Обрабатываем меню, если оно указано
    keyboard = None  
    if Block.menu:
        buttons = []        
        # Создаем кнопки из меню
        for button_data in Block.menu:
            callback = button_data["callback"]            
            # Проверяем наличие "https" в callback
            if callback=="BOGDAN_URL":   callback = BOGDAN_URL
            elif callback=="DONNA_URL":   callback = DONNA_URL
            elif callback=="UNILIV_URL":   callback = UNILIV_URL
            elif callback=="AXIOM5_URL":   callback = AXIOM5_URL 
            elif callback=="AXIOM0_URL":   callback = AXIOM_URL             
            text=button_data["caption"]
            
            if "https" in callback:                
                # Заменяем создание кнопки на создание с использованием url
                button = InlineKeyboardButton(
                    text=text,
                    url=callback  # Используем параметр url
                )
            else:                
                button = InlineKeyboardButton(
                    text=text,
                    callback_data=callback
                )
            
            buttons.append([button])  # Каждый button в своей строке
        keyboard = InlineKeyboardMarkup(buttons)
   
    print("Keyboard > ", str(keyboard).split('((')[-1])
    return Block.text, keyboard, picture_path

# def GET_BONS(pays:int=0):
    # return BONES[pays]
    # if pays>0:
        # return BONES[pays-1]
    # else:
        # return 0 


def REFRESHPART():
    global DONNA_URL, UNILIV_URL, AXIOM5_URL, AXIOM_REF    
    try:
        if Get_DONNA_URL(): DONNA_URL = Get_DONNA_URL()
        if Get_UNI_URL(): UNILIV_URL = Get_UNI_URL()
        if Get_AXI5M_URL(): AXIOM5_URL = Get_AXI5M_URL()
        if Get_AXI0M_REF(): AXIOM_REF = Get_AXI0M_REF()
        # AXIOM_URL = Get_AXI0M_URL()
    except Exception as e: print(e)   





def Get_Block(block_name):

    # Проверяем, что LIFE_BLOCK существует и не пуст
    # print (LIFE_BLOCK)
    if not LIFE_BLOCK:
        return None
    
    REFRESHPART()
    # print('1ok')
    # Определяем тип block_name один раз
    if isinstance(block_name, str):        key = 'title'
    elif isinstance(block_name, int):      key = 'id'
    else:                               return None  # Возвращаем None, если тип block_name некорректный
    # print('2ok')
    # Ищем блок по ключу
    message = next((block for block in LIFE_BLOCK if block.get(key) == block_name), None)
    # print('3ok')
    # Если блок не найден, возвращаем None
    if message is None:         return None
    # print('4ok')
    # Создаем и возвращаем объект TEXTBLOCK
    return TEXTBLOCK(
        item_id=message.get('id'),
        title=message.get('title'),
        text=message.get('ru'),
        picture=message.get('picture'),
        menu=message.get('menu')
    )
    
    
    

def LOG_DIC_INITY(bot_name, art_dir, artblock_dir):
    global BOT_NAME, ART_DIR, ARTBLOK_DIR
    BOT_NAME = bot_name
    ART_DIR = art_dir
    ARTBLOK_DIR = artblock_dir
    return BOT_NAME
 
def del_update_flag(file_flag):
    print(f">DUF< {file_flag} задушен 👹")
    os.remove(file_flag) 

def ESU(text):
    text = str(text)
    count = text.count('_')
    if (count>0) and (count % 2 != 0): # нечет
        text+='_'
    # return text.replace('_', '')
    return text

# def ArtBlock(title) -> str:
    # if title in ARTBOOK:
        # return ARTBOOK[title]   

def GetArt(pic:str):
    return None
    # print("GetArt> pic > ", pic)
    # art_pic = ArtBlock(pic)
    # print("GetArt> art_pic > ", art_pic)
    # pic_file = os.path.join(ART_DIR, art_pic)
    # print("GetArt> pic_file > ", pic_file)
    # ready = pic_file if os.path.isfile(pic_file) else None
    # return ready
  
def CYFER(message):
    number_icons = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣'   }
    beautiful_message = ''.join(number_icons.get(char, char) for char in message)
    return beautiful_message    
    
   

def Create_user_folders(mod_dir, user_folder):    
    path1 = mod_dir        # comon all users
    path2 = f'{path1}/{user_folder}'    # user
    os.makedirs(path1, exist_ok=True)
    os.makedirs(path2, exist_ok=True)
    return path1, path2
   
def Update_utc_zone(offset, context):    
    utc_str = get_utc_string(offset)
    Set_Var ('user_utc', utc_str, context)
    
def Update_User_ZONE(offset, context):
    Set_Var('user_tz', offset, context)
    # save_timezone(offset)
    # Update_step(19, context)
    Update_utc_zone(offset, context)     

def Get_Uid(context: ContextTypes.DEFAULT_TYPE):  
    return Get_Var('user_id', context)   
    
def Get_Var(variable:str, context: ContextTypes.DEFAULT_TYPE):  
    return context.user_data.get(variable)
    
def Get_VAR(variable:str, defvalue, context: ContextTypes.DEFAULT_TYPE): 
    return context.user_data.get(variable, defvalue)
    
def Set_Var(variable:str, value, context: ContextTypes.DEFAULT_TYPE):  
    context.user_data[variable] = value
    
def Update_step(index, context: ContextTypes.DEFAULT_TYPE):
    Set_Var('step', index, context)
     
async def UMR(text:str, update: Update):
    return await update.message.reply_text(text)   
   
def ESC(text: str):
    return html.escape(text)
    

async def SEX(text: str, context: ContextTypes.DEFAULT_TYPE, SENDER: int = None, DOC = None, EDIT = None, MENU = None, FORMAT: str = None):

    User_ID = Get_Uid(context)
    Send_ID = SENDER if SENDER else User_ID
    HYP, PARSE = None, None
    TEXT = text     
    if FORMAT:
        HYP = 'L' in FORMAT
        if 'B' in FORMAT:                                   
            PARSE = 'Markdown'
        elif 'H' in FORMAT:
            PARSE = 'HTML'
            TEXT = ESC(text)
    PARAMS = {
            'chat_id': Send_ID,
            'parse_mode': PARSE,
            'reply_markup': MENU,
        }
    
    if EDIT:
        M_ID = EDIT # M_ID = EDIT.message_id
        PARAMS['message_id'] = M_ID
        if DOC:
            PARAMS['caption'] = TEXT
            METHOD = context.bot.edit_message_caption
        else:
            if (text is None) and (MENU is not None):
                PARAMS.pop('parse_mode')
                METHOD = context.bot.edit_message_reply_markup
            else:
                PARAMS['text'] = TEXT
                METHOD = context.bot.edit_message_text

    elif DOC:
        if not isinstance(DOC, InputFile):
            DOC = InputFile(DOC)
        mime_type, _ = mimetypes.guess_type(DOC.filename)
        PARAMS['caption'] = TEXT
        if mime_type:
            if mime_type == 'audio/ogg':
                METHOD = context.bot.send_voice
                PARAMS['voice'] = DOC
            elif mime_type.startswith('audio'):
                METHOD = context.bot.send_audio
                PARAMS['audio'] = DOC
            elif mime_type.startswith('image'):
                METHOD = context.bot.send_photo
                PARAMS['photo'] = DOC
            elif mime_type.startswith('video'):
                METHOD = context.bot.send_video
                PARAMS['video'] = DOC
        else:
            METHOD = context.bot.send_document
            PARAMS['document'] = DOC
    else:
        METHOD = context.bot.send_message
        PARAMS['text'] = TEXT
        
        
    if HYP and (METHOD.__name__ in ['send_message', 'edit_message_text']):
        PARAMS['disable_web_page_preview'] = True    
        
    try:
        return await METHOD(**PARAMS)
    except Exception as e:
        print(f"SeM > {METHOD.__name__} > Ошибка отправки: {e}")
        print(f"SeM > Параметры > {PARAMS}")
        return None 
        
        
async def SEFoB(block, block_tex:str, context: ContextTypes.DEFAULT_TYPE):    
    block_pic = GetArt(block)    
    if block_pic:   # Отправляем фотографию
        print ("SEFoB: Найдена фотка, отправляем фото-блок")
        with open(block_pic, 'rb') as photo:
            await SEX(block_tex, context, DOC = photo, FORMAT = 'B') 
    else:
        print ("SEFoB: Фотка не найдена, отправляем текст")
        await SEX(block_tex, context, FORMAT = 'B')      

async def SEFoM(block, block_tex, keyb, context: ContextTypes.DEFAULT_TYPE):    
    block_pic = GetArt(block)    
    if block_pic:   # Отправляем фотографию
        print ("SEFoM: Найдена фотка, отправляем фото-блок c меню")
        with open(block_pic, 'rb') as photo:
            await SEX(block_tex, context, DOC = photo, MENU = keyb, FORMAT = 'B') 
    else:
        print ("SEFoM: Фотка не найдена, отправляем текст c меню")
        await SEX(block_tex, context, MENU = keyb, FORMAT = 'B')           
   
async def Make_MENU(text, buttons, context: ContextTypes.DEFAULT_TYPE):
    keyboard = Make_KEYB(buttons)
    return await SEX(text, context, MENU=keyboard)  # FORMAT = 'B') 
    
async def Make_MENB(text, buttons, context: ContextTypes.DEFAULT_TYPE):
    keyboard = Make_KEYB(buttons)
    return await SEX(text, context, MENU=keyboard, FORMAT = 'B')     

def Make_KEYB(buts):
    return InlineKeyboardMarkup(buts) 


def Comb_Reflink(code):
    return f"{BOT_NAME}?start={code}"    
    
def Save_Refdata(Code, Link, context: ContextTypes.DEFAULT_TYPE):
    Set_Var('user_refcode', Code, context) 
    Set_Var('user_reflink', Link, context)
    
def Regen_Link(context: ContextTypes.DEFAULT_TYPE):
    # BOT_NAME = Get_Var('BOT_NAME', context)
    Code  = Generate_Ref_Code() 
    Link =  Comb_Reflink(Code)    
    new = "новая " if Get_Var('user_reflink', context) else ""   
    text = f"🤝 Ваша {new}партнерская ссылка успешно получена 👍🏻"
    print (text)
    print (Link) 
    Save_Refdata(Code, Link, context)
 
# def Check_stix(LIFE_BOOK):
    # try:
        # if LIFE_BOOK[0].get('title') != 'stickers':
            # print ("Ошибка: Отсутствует ключ 'title' со значением 'stickers'")
            # return None
        # return sum(1 for key in LIFE_BOOK[0].keys() if key.isdigit())        
    # except Exception as e:
        # print (f"Ошибка: {str(e)}")
        # return None 
        
# async def Sendex_STICKER(sticker_name, context):
    # stixt = Send_STICKER(sticker_name, context)
    # if stixt:
        # mesid = Get_Var('mid_sticker', context)
        # if mesid:
            # await SEX(stixt, context, EDIT=mesid)           
        
# def Send_STICKER(sticker_name, context):
    # token = Get_Var('BOT_TOKEN', context)
    # uid = Get_Uid(context)
    # return Send_Stick(uid, sticker_name, token)
    
# def Send_Stick(chat_id, sticker_name, token):
    # global LIFE_BOOK
    # print(f"> Пришел запрос на вывод Стикера: {sticker_name} > ", end='')
    # sticker_id, stick_name = None, None
    # stickers = next((item for item in LIFE_BOOK if item.get('title') == 'stickers'), None)
    # if stickers is None:
        # print("Словарь стикеров не найден в LIFE-BOOK")
        # return None
    # if isinstance(sticker_name, (int, str)):
        # if isinstance(sticker_name, int) or sticker_name.isdigit(): # Если sticker_name - это число или строка с числом
            # index = str(int(sticker_name))
            # if index in stickers:
                # sticker_id = stickers[index]["id"]
                # stick_name = stickers[index]["name"]
        # else:   # Если sticker_name - это строка (название стикера)
            # for key, value in stickers.items():
                # if key != "title" and isinstance(value, dict) and value.get("name", "").lower() == sticker_name.lower():
                    # sticker_id = value["id"]
                    # stick_name = sticker_name
                    # index = key
                    # break
    # if sticker_id is None:
        # print(f"Стикера {sticker_name} нет в нашем словаре стикеров ((( ")
        # return None
    # print("ok")
    # stixt = f"🐹 Стикер:{index} > '{stick_name}'"
    # Send_Stik(chat_id, sticker_id, token)
    # return stixt    
    
def Send_Stik(chat_id, sticker_id, token):
    url = f"https://api.telegram.org/bot{token}/sendSticker"
    DATA = {
        'chat_id': chat_id,
        'sticker': sticker_id}
    response = requests.post(url, params = DATA)
    return response.json()     

            
async def Scroll_chat_down(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = Get_Uid(context)
    # Используем невидимый символ Unicode  # invisible_character = "\u200B"
    message = " "
    max_attempts = 2 
    # Отправляем сообщение с эмодзи и сохраняем его
    last_message = await context.bot.send_message(chat_id=user_id, text="⌛️")
    # await SEX("⌛️", context) # 
    
    print("@ Начали скроллинг.", end='', flush=True)
    for attempt in range(max_attempts):
        try:           
            print(".>.", end='', flush=True)
            await context.bot.send_message(
                chat_id=user_id,
                text=message,
                disable_notification=True)
            print("Скроллинг выполнен успешно @", flush=True)
            break
        except Exception as e:
            if attempt < max_attempts - 1:
                print("_", end='', flush=True)
                await Adelay(2)  # Ждем 3 сек перед следующей попыткой            
    print("Забили на скроллинг @", flush=True)    
    # Удаляем сообщение с эмодзи
    try:
        await delete_bot_message(last_message, context)
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")    
    return False       

async def delete_bot_message(message, context: ContextTypes.DEFAULT_TYPE):
    if message and hasattr(message, 'chat_id') and hasattr(message, 'message_id'):
        try:
            print(f"Пробуем удалить сообщение {message.message_id} в чате {message.chat_id}")
            await context.bot.delete_message(
                chat_id=message.chat_id,
                message_id=message.message_id
            )
            print("Сообщение успешно удалено")
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")
    else:
        print("Некорректный объект сообщения для удаления")





# def TextBlock(title) -> str:
    # global LIFE_BOOK
    # for message in LIFE_BOOK:
        # if message['title'] == title:
            # return message[LANG]
            # break
    # return None
 
async def MAKE_DAYBACK(context: ContextTypes.DEFAULT_TYPE): 
    await SEX("/start👉🏻Меню🕰Дня  /help👉🏻Помощь❓Команд", context)   

async def MAKE_REFBACK(context: ContextTypes.DEFAULT_TYPE):
    await SEX("🔰 Возврат в Реферальную Панель 👉🏻 /refer", context)
  
async def delete_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last_message = update.effective_message
    if last_message.from_user.id != context.bot.id:
        try: # Удаляем сообщение пользователя
            await context.bot.delete_message(
                chat_id=last_message.chat_id,
                message_id=last_message.message_id)
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")


def load_dict(ant_dict):
    print(f">>> {ant_dict} > ", end='')
    try:
        with open(ant_dict, 'r', encoding='utf-8') as f:
            dictt = json.load(f)
        print("СЛОВАРЬ ЗАГРУЖЕН")
        return dictt
    except FileNotFoundError:
        print("СЛОВАРЬ НЕ НАЙДЕН!")
        return None
    except json.JSONDecodeError:
        print("СЛОВАРЬ СЛОМАЛСЯ! проверь JSON в конфиге!")
        return None
    
def load_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print(">>> Конфиг загружен! ", end='')
        return config
    except FileNotFoundError:
        print(">>> Конфиг-файл не найден! Да и хрен с ним ")
        return None
    except json.JSONDecodeError:
        print(">>> Хреновый JSON в конфиге! Игнорируем его ")
        return None
 
 
 
# async def SEB(text: str, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return SEM BOLD
        # result = await context.bot.send_message(chat_id=u_id, text=text, parse_mode='Markdown')
        # result = await context.bot.send_message(chat_id=u_id, text=text, parse_mode='MarkdownV2')
        # return result
    # except Exception as e:
        # print(f"SEB - Ошибка отправки сообщения: {e}")
        # return None    


# async def SEL(text: str, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return SEM Without LINK
        # result = await context.bot.send_message(chat_id=u_id,text=text,disable_web_page_preview=True)
        # return result
    # except Exception as e:
        # print(f"SEL - Ошибка отправки сообщения: {e}")
        # return None


            # text = ESC(text),
            # parse_mode='HTML',
        

        
 
        
# async def ESB(m_id, new_text, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return ESM BOLD
        # result = await context.bot.edit_message_text(
            # chat_id = u_id,
            # message_id = m_id,
            # text=new_text,
            # parse_mode='Markdown')
        # return result
    # except Exception as e:
        # print(f"ESB - Ошибка отправки сообщения: {e}")
        # return None
        

# async def SEFI(cap: str, photo, u_id, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return Send_Photo BOLD
        # result = await context.bot.send_photo(chat_id=u_id, photo=photo, caption=cap)  
        # return result
    # except Exception as e:
        # print(f"SEFI - Ошибка отправки картинки: {e}")
        # return None  




# async def SEFB(cap: str, photo, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return Send_Photo 
        # result = await context.bot.send_photo(
            # chat_id = u_id,
            # photo = photo,
            # caption = cap,
            # parse_mode = 'Markdown')  
        # return result
    # except Exception as e:
        # print(f"SEFB - Ошибка отправки картинки: {e}")
        # return None        


 
# async def SEIM(text, keyboard, u_id: int, context: ContextTypes.DEFAULT_TYPE):
    # try:    # return ` SEMM to ID
        # sent_message = await context.bot.send_message(
            # chat_id = u_id,
            # text = text,
            # reply_markup = keyboard)
        # return sent_message
    # except Exception as e:
        # print(f"SEIM - Ошибка отправки сообщения: {e}")
        # return None         

# async def SEMM(text, keyboard, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return SEM + MENU
        # sent_message = await context.bot.send_message(
            # chat_id = u_id,
            # text = text,
            # reply_markup = keyboard)
        # return sent_message
    # except Exception as e:
        # print(f"SEMM - Ошибка отправки сообщения: {e}")
        # return None
# async def ESMM(m_id, new_text, new_keyboard, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return ESM + MENU
        # sent_message = await context.bot.edit_message_text(
            # chat_id = u_id,
            # message_id = m_id,
            # text = new_text,
            # reply_markup = new_keyboard)  
        # return sent_message
    # except Exception as e:
        # print(f"ESMM - Ошибка редакции сообщения: {e}")
        # return None

# async def SEBM(text, keyboard, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return SEB + MENU
        # sent_message = await context.bot.send_message(
            # chat_id = u_id,
            # text = text,
            # parse_mode='Markdown',
            # reply_markup = keyboard)
        # return sent_message
    # except Exception as e:
        # print(f"SEBM - Ошибка отправки сообщения: {e}")
        # return None
# async def ESBM(m_id, new_text, new_keyboard, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return EDIT SEB + MENU
        # sent_message = await context.bot.edit_message_text(
            # chat_id = u_id,
            # message_id = m_id,
            # text = new_text,
            # parse_mode='Markdown',
            # reply_markup = new_keyboard)  
        # return sent_message
    # except Exception as e:
        # print(f"ESBM - Ошибка редакции сообщения: {e}")
        # return None 
        
# async def SEFM(cap: str, photo, keyboard:int, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return Send_Photo to ID + MENU
        # result = await context.bot.send_photo(chat_id=u_id, photo=photo, caption=cap, reply_markup=keyboard)  
        # return result
    # except Exception as e:
        # print(f"SEFM - Ошибка отправки сообщения: {e}")
        # return None
        
# async def SEFBM(cap: str, photo, keyboard:int, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return Send_Photo to ID + MENU
        # result = await context.bot.send_photo(
            # chat_id=u_id, 
            # photo=photo, 
            # caption=cap,
            # parse_mode='Markdown',            
            # reply_markup=keyboard)  
        # return result
    # except Exception as e:
        # print(f"SEFBM - Ошибка отправки сообщения: {e}")
        # return None

# async def SELM(text, keyboard, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return SEM + MENU - LINK
        # sent_message = await context.bot.send_message(
            # chat_id = u_id,
            # text = text,
            # disable_web_page_preview=True,
            # reply_markup = keyboard)
        # return sent_message
    # except Exception as e:
        # print(f"SELM - Ошибка отправки сообщения: {e}")
        # return None 
# async def SEHM(text, keyboard, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return SEMM in HTML+web+escape
        # sent_message = await context.bot.send_message(
            # chat_id = u_id,
            # text = ESC(text),
            # parse_mode='HTML',
            # reply_markup = keyboard)
        # return sent_message
    # except Exception as e:
        # print(f"SEHM - Ошибка отправки сообщения: {e}")
        # return None   
# async def SELHM(text, keyboard, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return SEMM in HTML+web+escape -link
        # sent_message = await context.bot.send_message(
            # chat_id = u_id,
            # text = ESC(text),
            # parse_mode='HTML',
            # disable_web_page_preview=True,
            # reply_markup = keyboard)
        # return sent_message
    # except Exception as e:
        # print(f"SELHM - Ошибка отправки сообщения: {e}")
        # return None        
# async def SELBM(text, keyboard, context: ContextTypes.DEFAULT_TYPE):
    # u_id = Get_Uid(context)
    # try:    # return SEBM -link
        # sent_message = await context.bot.send_message(
            # chat_id = u_id,
            # text = text,
            # parse_mode='Markdown',
            # disable_web_page_preview=True,
            # reply_markup = keyboard)
        # return sent_message
    # except Exception as e:
        # print(f"SELBM - Ошибка отправки сообщения: {e}")
        # return None 
 
 
 
 
 
 
 
 
 
 
# stime = f"{int(hours):02} часов {int(minutes):02} минут"  # ftime = f"{stime} {int(seconds):02} секунд" 

# Попытка преобразования строки в объект datetime
    # try:
# Преобразование значения в тип datetime
        # if isinstance(time_string, str):
            # if '+' in time_string:
                # time_string = time_string.split('+')[0]  # Удаление информации о часовом поясе            
# Пробуем сначала формат с микросекундами
            # try:
                # user_stime_obj = datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S.%f')
            # except ValueError:
# Если не получилось, пробуем формат без микросекунд
                # user_stime_obj = datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')        
        # elif isinstance(time_string, datetime):
            # user_stime_obj = time_string
        # else:
            # print(f"Unexpected user_stime type: {type(time_string)}")
            # return None
    # except ValueError:
        # print(f"Unable to parse user_stime: {time_string}")
        # return None      
# Преобразование user_stime в offset-aware datetime
# user_stime_obj = user_stime_obj.replace(tzinfo=timezone.utc)        
    # return user_stime_obj    
    
#def Parse_Report(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    last_message = update.effective_message
    #message_id=last_message.message_id
#    print("Идет парсинг РЕПОРТ сообщения > ") 
#    if last_message:
#        sender_id = last_message.chat_id
#        print(f"-sender_id: {sender_id}")
#        Set_Var('sender_id', sender_id, context)        
#        text = last_message.caption
#        print(f"-message.text: {text}")        
#        sender_name = Find_IM(text)
#        print(f"-sender_name: {sender_name}")
#        Set_Var('sender_name', sender_name, context) 
#        sender_day = Find_DAY(text)
#        print(f"-sender_day: {sender_day}")
#        Set_Var('sender_day', sender_day, context) 
#        file = last_message.document       
#        return file
#    else:
#        return None
        
#async def Download_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#    file = Parse_Report(update, context)
#    if file:
#        file_id = file.file_id
#        file_name = file.file_name 
#        new_file = await context.bot.get_file(file_id)
#        os.makedirs(MODERATOR_DIR, exist_ok=True)
#        file_path = os.path.join(MODERATOR_DIR, file_name)
        #new_file.download(file_path)
#        file_data = await new_file.download_as_bytearray() # Загрузка файла в виде bytearray
#        with open(file_path, 'wb') as f:
#            f.write(file_data)       
#        return file_path
#    else:
#        return None


#def open_os(file_path):
#    # Открываем в браузере
#    if platform.system() == 'Windows':
#        os.startfile(file_path)
#    elif platform.system() == 'Darwin':  # macOS
#        os.system(f'open "{file_path}"')
#    elif platform.system() == 'Linux':
#        if "ANDROID_ROOT" in os.environ:  # Проверка на Android
#            try:
#                # Используем intent для открытия файла на Android
#                subprocess.call(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', f'file://{file_path}'])
#            except Exception as e:
#                print(f"Ошибка при открытии файла на Android: {e}")
#        else:
#            # Linux и другие Unix-подобные системы
#            os.system(f'xdg-open "{file_path}"')
#    else:
#        print("Неподдерживаемая операционная система")

#async def SEND_PACK(zip_name, context: ContextTypes.DEFAULT_TYPE):
#    text = "👉🏻 Отправка Модератору"
#    send_id =  Get_Var ('user_id', context) if SELF else MODERATOR_ID
#    #result = Send_zip(NOTIFY_BOT_TOKEN, send_id, zip_name)
#    message, keyboard = Prep_MOC (zip_name, context)        
#    result = Send_ZIM(NOTIFY_BOT_TOKEN, send_id, zip_name, message, keyboard)
#    if result==200:
#        return 1
#    else:
#        print ("Отправка Архива  - ОШИБКА сбой отправки")
#        return 0
