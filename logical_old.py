dev_ver = 437
# 2. 4ч28 дней стат3ус прогерс
pub_ver = 'beta 2'
VER = f"{pub_ver}🧩{dev_ver}"
import os, sys, json, random, traceback
from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes
from lifeman import *
# from lifeman import AXIOM_URL
from active import *
from passive import *
from moderator import *
from ambacron import *
from answers import *
from temporal import *
# from reports import DetaledReport
# from free11fray import AQnit, AIQue, draw_image
from free11ray import AQnit, INHA_TEX
# from fre0lib import Pic_Find, Parse_TeLinx, ASPLIT, format_to_md, Upchate, Gechate
from fre0lib import Upchate, Gechate
from fre0gen import TuneGenPath
# Ring_STX = 'CAACAgEAAxkBAAENB8ZnIG6wpYSeyiuwy27Bjt62hys9aAACNgMAAhOiGEQpRM8rzoHLZDYE'
# KEYDRAW = ["рисуй", "сгень", "t2i", "imagine"]
RANGS = "ИГРОК", "РЕВИЗОР", "АДМИНИСТРАТОР", "МОДЕРАТОР" # Игорь 5750294303
ADMINS = [6794691889, 456781641, 458972922]  # John, Bogdan, Olesa
MODERATORS = [456781641, 6794691889] # Bogdan, John
REVISORS = [1802577464, 458972922]   #  Gena Gorin
DEVELOPERS = {"Bogdan_Golos": 456781641, "John_Tesla": 6794691889}
SRC_dir = "d:\\COMON\\DEV\\life-book"
MODERATOR_DIR = 'LIFE-BOOK'
BRAND_RUS = ('Книга жизни', 'КНИГА ЖИЗНИ')
TARGET_DATE = get_target_date(2025, 5, 5)
LIFE_CHAT_ID = -1002232747079 # чат Жизнь
PAY_CHAT_id = -1002562493765 # чат Оплата
GPG_CHAT_id = -1001788044296 # чат ГЖП группа проекта Жизн
DEV_CHAT_id = LIFE_CHAT_id
MAX_STIX = 53
MAX_DAYS = 28
ITEMS_PER_PAGE = 4
# TEST_url = "https://telegra.ph/Kniga-ZHizni-08-11"

TASKS = [
        "Радость дня 😊",
        "Благодарность дня 🙏",
        "❓ Вопрос дня 💡"
    ]
TIMEZONES = {
    # 'Гринвич utc0': +0,      # UTC0
    'Нью-Йорк -5': -5, # UTC-5
    'Париж +1': +1,    # UTC+1
    'Берлин +2': +2,   # UTC+2
    'Москва,Киев +3': +3,   # UTC+3
    'Дубай +4': +4,    # UTC+4
    'Алматы +6': +6,   # UTC+6
    'Бангкок +7': +7,  # UTC+7
    'Токио +9': +9    # UTC+9
    }

# ROLES = [ 'Роль Игрока', 'УЧАСТНИК', 'СПЕЦИАЛИСТ', 'ПРЕДПРИНИМАТЕЛЬ', 'ИНВЕСТОР' ]
ROLES = [ 'Роль Игрока', 'УЧАСТНИК', 'СПЕЦИАЛИСТ', 'ПРЕДПРИНИМАТЕЛЬ' ]
# User_Tarifes = ['FREE', 'PRO-3', 'PRO-33', 'PRO-99']
User_Tarifes = ['FREE', 'PRO']
# TARIF = [3, 33, 99]
# TARIF = [0, 10, 40, 60, 99, 100]
# BONES = [0, 1, 3, 5, 10, 20]





DEMO = not True
PUB  = not True # СЕРВЕР
REV  = not True # * РЕВИЗОР
ADM  = not True # ** АДМИНИСТРАТОР
DEV  = not True # *** МОДЕРАТОР
SU   = not True # (*) НЕ ИГРОК
MOD_TYPE = 1   # авто Модератор 1=Богдан 2=Тесла
CORE_UPD = 0
N_TAX = len(TASKS)
MOFO = None
LIFE_BLOCK = None

async def GLUBDATE(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    Set_Var ('user_id', user_id, context)
    Upchate(user_id, context)
    TuneGenPath(user_id)
    user_path = Get_Var ('user_path', context) 
    Set_UP(user_id, user_path)
    uuu = Gechate(context)
    print(">> test gechate...", uuu)    


async def START_AGAIN(warn:str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await GLUBDATE(update, context)
    
    Set_Var('mid_Show_Time', None, context)
    Set_Var('mid_Ask_Zone', None, context)
    Update_step(19, context)
    if (warn is not None) and (warn!=''):
        await SEX(warn, context, FORMAT='B')
        Sdelay(1)

    # Send_STICKER("доброе утро", context)    #  команда СТАРТ
    print(">> Инициация бота пользователем > запрос данных...")
    uf_IsNew = not Check_User(context)  # проверяем юзера
    Set_Var('uf_IsNew', uf_IsNew, context)
    if uf_IsNew:  # new user
        await START_JOIN (update, context)
    else:  # old user
        await START_LIFE (update, context)

async def START_JOIN(Update, context: ContextTypes.DEFAULT_TYPE):
    Update_step(18, context)
    print("Первых вход Юзера, приветствие, регистрация...")
    await SEX_PRO('JOIN1', context)

async def START_JOIN2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("РЕГ > Ожидается Ввод юзером псевдонима...")
    Update_step(1, context)
    await SEX_PRO('JOIN2', context)
    
async def START_JOIN2_GOT(msg:str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Запущен процесс регистрации")
    Set_Var ('user_nick', msg, context)
    Update_step(2, context)    
    await START_JOIN3(update, context)


async def START_JOIN3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # print("Ожидается выбор РОЛИ юзером ...")
    print("Теперь у всех 1 роль на входе")
    await SETUP_ROLE(1, update, context)    
    
        # await SEX_PRO('JOIN4', context)
    # lives = 3
    # message_text, keyboard, picture_path = Make_Block('JOIN3')
    # message_text = message_text.format(lives)
        # User_Name = user_name, User_Role = user_role     )
    # Block_Pk = message_text, keyboard, picture_path
    # await SEX_PROD(Block_Pk, context)
    

async def SETUP_ROLE(role_index, update: Update, context: ContextTypes.DEFAULT_TYPE): 
    print("Сохраняем РОЛЬ в МИДВАР ...")
    role = ROLES[role_index]
    Set_Var('user_role', role, context)
    text = f'▶️ Выбрана роль: {role}'
    await SEX(text, context, FORMAT='B')
    await START_JOIN4(update, context)



async def START_JOIN4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Ожидается выбор Час. Пояс\Зона ...")
    # проверяем Часовую Зону для ЮЗЕРА
    offset = Get_Var ('user_tz', context)
    print (">After_Init> Ищем timezone в MIDVAR: ", offset)
    if offset is None:
        print (">After_Init> Часовой ПОЯС не задан > Пока ставим UTC=0")
        offset = 0        # Update_User_ZONE(offset, context)
    Update_User_ZONE(offset, context)
    print (">After_Init> Обновляю ТЗ на основе offset=", offset)    
    # await SEX_PRO('JOIN3', context)    
    await Ask_TZ(update, context)
    # await POST_PREP(update, context)
    
   

async def POST_PREP(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    uf_IsNew = Get_Var('uf_IsNew', context)
    offset = Get_Var('user_tz', context)
    if not uf_IsNew:
        if offset: save_timezone(offset)
        return await START_LIFE(update, context)
        
    print ("Регистрируем Юзера")
    user_id = await Reg_User(update, context)
    Set_Var('uf_IsNew', None, context)
    print ('Тестируем вторичный user_id=', user_id)
    if not user_id or (user_id<1):
        print ('Ошибка возврата user_id')
    else:
        print ('Обновляем user_id !!!')
        Set_Var ('user_id', user_id, context)
    # Init_Answers()
    # offset = Get_Var('user_tz', context)
    save_timezone(offset)
    role = Get_Var('user_role', context)
    save_role(role)       
    
    INCRES = CRON_AMBA1(context)
    print("СТАРТУЕМ КРОНы > ", INCRES)
    await After_Init(context)
    await START_LIFE(update, context)  

    

async def START_LIFE(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = Get_Var ('user_nick', context)
    print(f"Пользователь: {user_name} прошел авторизацию")
    # user_role = get_role()
    # user_lives = get_credos(1)
    # Blok = Get_Block(5)
    # forma = f'User_Name = {user_name}, User_Role = {user_role}'
    # await SEX_PRO2('START1',forma.split(','), context) , lives = user_lives 
    Update_step(19, context)
    message_text, keyboard, picture_path = Make_Block('START1')
    message_text = message_text.format(User_Name = user_name)        
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context)
    

async def START_PRO(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await INPAY(context)
    # await SEX_PRO('LB_INPAY', context)   
    await START_PRO2(context)
    
async def START_PRO2(context: ContextTypes.DEFAULT_TYPE):
    # user_role = get_role()
    # LB_PROF = 'LB_PROFY+' if '+' in user_role else 'LB_PROFY'
    # LB_PROF = 'LB_PROFY+' if IsUserPREM() else 'LB_PROFY'
    await SEX_PRO('START2', context) 


async def Start_ROLES(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await Scroll_chat_down(update, context)
    Update_step(19, context)
    user_live = get_credos(1)
    if await END_DAY(context): return
    # if await FINALIZE(context): return
    FILL_UP = '\n📗 *Заполнить* _Дневник Осознанности_ 👉 /daily'
    user_role = get_role()
    message_text, keyboard, picture_path = Make_Block('LB_STATUS')
    user_vita = get_credos(2)
    day = Get_User_Day(context)
    
    dpas = Get_VAR('day_pass', '0', context)
    geoday = int(dpas) + 1
    
    # wday = get_uwork()
    week = get_uweek()
    dole = get_credos(4)
    user_refs = get_ref_count()
    ref_code = get_ref_code()
    taskflags = Check_user_flags(day)
    uf_ALL_fin = Is_ALL_fin(day, taskflags)    
    status = jet_status(context)
    User_Rating = get_rating()
    ref_link = Comb_Reflink(ref_code)
    Set_Var('user_reflink', ref_link, context) 
    fillup = '' if uf_ALL_fin else FILL_UP
    leftday = MAX_DAYS - day
    leftdays = pluralize_ru(leftday, "день", "дня", "дней")
    message_text = message_text.format( 
        # User_Tarif = User_Tarif,
        # User_Vita = user_vita, 
        # User_Refs = user_refs, 
        # Ref_code = ref_code, 
        # Ref_link = ref_link,       
        User_Role = user_role, 
        User_Rating = User_Rating,
        User_Live = user_live, 
        geoday = geoday,
        maxday = MAX_DAYS,        
        status = status,
        fillup = fillup,
        day = day,
        dole = dole,
        leftday = leftdays,
        week = week
        )
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context)
    


async def FINALIZE(context: ContextTypes.DEFAULT_TYPE):  
    # day_work = get_uwork()
    day = Get_User_Day(context)
    if day < MAX_DAYS:
        return False
        
    await SEX_PRO('FINAL', context)       
    return True

# async def FINALIZE_by_DAY_Old(context: ContextTypes.DEFAULT_TYPE):  
    # day = Get_User_Day(context)
    # if day<MAX_DAYS:  return False
    # await SEX_PRO('FINAL', context)       
    # return True


async def END_DAY(context: ContextTypes.DEFAULT_TYPE):  
    user_live = get_credos(1)
    if user_live and user_live<=0:
        await END_book(context)
        return True  
    else:
        await TUNE_DAY(context)
        return await FINALIZE(context)   
    
    
async def TUNE_DAY(context: ContextTypes.DEFAULT_TYPE):
    INCRES = CRON_AMBA1(context)
    print("ЧЕКАЕМ КРОНы 1-INCRES> ", INCRES)
    FLAG_CELC = CRON_AMBA2(context)
    print("ЧЕКАЕМ КРОНы 2-CELC> ", FLAG_CELC)
    # if INCRES:
        # print("Был переход дня - обновляем триггер бонуса Set_DOLE_FP=False")
        # Set_DOLE_FP(False)    
    


async def START_BOOK(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    await START_BOOKIN(context)
    
async def START_BOOKIN(context: ContextTypes.DEFAULT_TYPE):    
    # await SEX_PRO('START3', context) 
    # await Scroll_chat_down(context.update, context)
    # user_live = get_credos(1)
    # if user_live<=0:
        # return await END_book(context)
    if await END_DAY(context): return    
    pays = get_pays()
    # print ('PAYS=', pays)
    User_Tarif = User_Tarifes[pays] if pays else pays
    message_text, keyboard, picture_path = Make_Block('LB_START')
    message_text = message_text.format(User_Tarif = User_Tarif)
        # User_Name = user_name, User_Role = user_role     )
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context)



async def START_INVEST(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    # await SEX_PRO('INVEST', context)
    preme = Get_User_Tarife(get_pays())
    dole, vita = get_credos(4), get_credos(2)
    # pree = f"🎩 Инвесторский статус: {preme}\n"
    message_text, keyboard, picture_path = Make_Block('INVEST')
    message_text = message_text.format( preme = preme,  
         dole = dole, User_Vita = vita )
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context)
  
    
async def GO_SHOP(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await SEX_PRO('LB_SHOP', context)

async def START_NEW(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await SEX_PRO('LB_START', context)
    # await Start_DAY (update, context)

async def START_DAY(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user_live = get_credos(1)
    # if user_live<=0:
        # return await END_book(context)
    if await END_DAY(context): return        
    message_text, keyboard, picture_path = Make_Block('LB_DAILY')
    # message_text = message_text.format(forma)
    new_keyb = await Send_Task_Buttons(update, context)
    Block_PAK = message_text, new_keyb, picture_path
    await SEX_PROD(Block_PAK, context)    

async def INPAY(context: ContextTypes.DEFAULT_TYPE):    
    Moderator_ID = Get_Var ('MOD_ID', context)
    text = "Игрок перешел к ОПЛАТЕ входа ПРОФИ"
    prepay_text = Prep_MOC4(context) + '\n' + text    
    # await SEX(user_text, context, FORMAT='B') # СООБЩ юзеру 
    
    await SEX(prepay_text, context, FORMAT='B', SENDER=Moderator_ID) # СООБЩ Моду
    MSG = await SEX(prepay_text, context, FORMAT='B', SENDER=PAY_CHAT_id) # СООБЩ в ЧАТ 
    # await BugSpy_Handler(MSG, context) # СООБЩ в ЧАТ
    
    Set_Var ('mid_Start_Text', prepay_text, context) 
    Set_Var ('mid_Start_Rules', MSG.message_id, context)
    print ('Записано mid_Start_Rules=', MSG.message_id)
    # Set_Var ('mid_Start_Rumod', MSG2.message_id, context)
    # print ('Записано mid_Start_Rumod=', MSG2.message_id)
    await SEX_PRO('LB_PAKET', context)
    # await SEX_PRO('LB_INPAY', context)
    

async def IN_TARIF(tarr:int, context: ContextTypes.DEFAULT_TYPE):
    Moderator_ID = Get_Var ('MOD_ID', context)
    price, vitas, lives = get_tariff_infoby_index(tarr-1)
    tarif = f'`{price}` USDT' if tarr>0 else ''   
    
    Set_Var ('user_tarif', tarr, context)
    text = f"Игрок выбрал {tarr} ТАРИФ - {tarif}"
    prepay_text = Prep_MOC4(context) + '\n' + text    
    # await SEX(user_text, context, FORMAT='B') # СООБЩ юзеру    
    
    # MSG2 = Get_Var ('mid_Start_Rumod', context)
    MSG = Get_Var ('mid_Start_Rules', context)
    text = Get_Var ('mid_Start_Text', context) + '\n' + text 
    Set_Var ('mid_Start_Text', text, context)
    
    if MSG:
        await SEX(text, context, FORMAT='B', EDIT = MSG, SENDER=PAY_CHAT_id)
    else:      
        MSG = SEX(prepay_text, context, FORMAT='B', SENDER=PAY_CHAT_id) # СООБЩ в ЧАТ
        Set_Var ('mid_Start_Rules', MSG.message_id, context)
   
    # await SEX_PRO('LB_PAKET', context)
    # await SEX_PRO('LB_INPAY', context)    
    message_text, keyboard, picture_path = Make_Block('LB_INPAY')
    message_text = message_text.format(
        tar = tarr, payment = tarif)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context)   
    
   
async def INPAIMENT(context: ContextTypes.DEFAULT_TYPE):
    Moderator_ID = Get_Var ('MOD_ID', context)
    user_name = Get_Var ('user_nick', context)
    text = 'Для подтверждения оплаты нужен *чек или квитанция* об оплате\n_Отправьте чек в чат в виде изображения или PDF документа_'
    user_text = '*Уважаемый участник!*\n' + text    
    await SEX(user_text, context, FORMAT='B') # СООБЩ юзеру 
    
    text = 'Игрок ☑️ Отправляет квитанцию'
    # text = 'Игрок ✅ Подтверждает Оплату!'
    prepay_text = Prep_MOC4(context) + '\n' + text   
    text2 = Get_Var ('mid_Start_Text', context)+ '\n' + text     
    # Set_Var ('mid_Start_Text', text2, context)
    MSG = Get_Var ('mid_Start_Rules', context)
    # MSG2 = Get_Var ('mid_Start_Rumod', context)
    
    if MSG:
        MSG2 = await SEX(text2, context, FORMAT='B', EDIT = MSG, SENDER=PAY_CHAT_id) # СООБЩ в ЧАТ
        # Set_Var ('mid_Start_Text', text2, context)
    else:      
        MSG2 = await SEX(prepay_text, context, FORMAT='B', SENDER=PAY_CHAT_id) # СООБЩ в ЧАТ

    # if MSG2:        
        # await context.bot.forward_message(chat_id=PAY_CHAT_id, 
            # from_chat_id=MSG2.chat.id, message_id=MSG2.message_id)

    
    Update_step(9, context)
    
    # await SEX(prepay_text, context, FORMAT='B', SENDER=PAY_CHAT_id) # СООБЩ в ЧАТ
    # await BugSpy_Handler(MSG, context)    
    # user_name = Get_Var ('user_nick', context)
    # MSG = await SEX(f'Пользователь *{user_name}* подтверждает оплату ✅', context)
    # await BugSpy_Handler(MSG, context)
    # await START_PRO2(update, context)

async def INPAID(context: ContextTypes.DEFAULT_TYPE):
    Moderator_ID = Get_Var ('MOD_ID', context)
    # await SEX('Оплата успешна ✅', context)
    # text = 'Менеджер ✅ Утвердил Оплату'
    text = 'Игрок ✅ Отправил квитанцию'
    prepay_text = Prep_MOC4(context) + '\n' + text
    MSG = Get_Var ('mid_Start_Rules', context)
    if MSG:
        # text3 = mids if mids else 
        text3 = Get_VAR ('mid_Start_Text', '', context) 
        text3 += '\n' + text 
        MSG2 = await SEX(text3, context, FORMAT='B', EDIT = MSG, SENDER=PAY_CHAT_id) # СООБЩ в ЧАТ
        Set_Var ('mid_Start_Text', text3, context)
    else:      
        MSG2 = await SEX(prepay_text, context, FORMAT='B', SENDER=PAY_CHAT_id) # СООБЩ в ЧАТ

    # chat_username = "your_chat_username"  # Юзернейм чата (без @)
    print('Репорт MSG=', MSG2)
    print('Репорт MSGid=', MSG2.message_id)
    chat_id = str(PAY_CHAT_id).replace('-100', '')
    message_link = f"https://t.me/c/{chat_id}/{MSG2.message_id}"
    print('Репорт MSG LINK=', message_link)
    # await SEX(prepay_text, context, FORMAT='B', SENDER=LIFE_CHAT_id) # СООБЩ в ЧАТ
    # сигнал Модератору
    text, keyboard  = Prep_MOC5(message_link, context)
    await SEMOD(text, keyboard, context)    
    # сигнал Чат
    # await SEX(prepay_text, context, FORMAT='B', SENDER=LIFE_CHAT_id) # СООБЩ в ЧАТ      
    # сигнал Юзеру
    mess = f'*Благодарим за оплату!*\nОжидайте подтверждения о получении перевода!\n_Проверка проходит в ручном режиме, поэтому может потребоваться немного времени_'    
    await SEX(mess, context, FORMAT='B')    
    # await BugSpy_Handler(mess, context)     
    # await START_PRO2(context)
    Sdelay(3)
    await START_BOOKIN(context)


async def FILL_DAY(context: ContextTypes.DEFAULT_TYPE):
    user_name = Get_Var ('user_nick', context)
    dole = get_credos(4)
    # dole = get_uwork()
    message_text, keyboard, picture_path = Make_Block('LB_BONUS')
    message_text = message_text.format(name = user_name, maxday = MAX_DAYS)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context)

async def DONNA_SET(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await SEX('Задайте свою *партнерскую ссылку проекта DONNA* для приглашения друзей.\n_Для этого ▶️ отправьте в чат Вашу реферальную ссылку проекта_ *Donna AI* 👇🏻', context, FORMAT='B')
    Update_step(11, context) # last silence Step
    
async def UNI_SET(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await SEX('Задайте свою *партнерскую ссылку проекта UNILIVE* для приглашения друзей.\n_Для этого ▶️ отправьте в чат Вашу реферальную ссылку проекта_ *UniLIVE* 👇🏻', context, FORMAT='B')
    Update_step(18, context) # last silence Step

async def AXI0_SET(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await SEX('Задайте свой *партнерский логин проекта AXIOMA* для приглашения друзей.\n_Для этого ▶️ отправьте в чат Ваш партнерский логин проекта_ *AXIOMA* 👇🏻', context, FORMAT='B')
    Update_step(21, context) # last silence Step



async def AXI5_SET(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    await SEX('Задайте свою *партнерскую ссылку проекта LIFE5* для приглашения друзей.\n_Для этого ▶️ отправьте в чат Вашу реферальную ссылку проекта_ *LIFE5* 👇🏻', context, FORMAT='B')
    Update_step(22, context) # last silence Step


async def DONNA_RUN(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await DONNA(context)
    

async def DONNA(context: ContextTypes.DEFAULT_TYPE):
    # name = Get_Var ('user_nick', context)
    # await SEX_PRO('LB_DONNA', context)
    donna_url = Get_DONNA_URL()
    message_text, keyboard, picture_path = Make_Block('LP_DONNA')
    message_text = message_text.format(donna_url = donna_url)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context)

async def UNI_RUN(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await UNILIVE(context)
    

async def UNILIVE(context: ContextTypes.DEFAULT_TYPE):
    # name = Get_Var ('user_nick', context)
    # await SEX_PRO('LB_UNI', context)
    uni_url = Get_UNI_URL()
    message_text, keyboard, picture_path = Make_Block('LP_UNI')
    message_text = message_text.format(uni_url = uni_url)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context)

async def AXIOM5_RUN(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await AXIOM5(context)

async def AXIOM5(context: ContextTypes.DEFAULT_TYPE):
    # name = Get_Var ('user_nick', context)
    # await SEX_PRO('LP_5LIFE', context)
    axi5_url = Get_AXI5M_URL()  # ведет на 5 Ж версию
    message_text, keyboard, picture_path = Make_Block('LP_5LIFE')
    message_text = message_text.format(axi5_url = axi5_url)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context)

async def AXIOM0_RUN(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await AXIOM0(context)

async def AXIOM0(context: ContextTypes.DEFAULT_TYPE):
    # await SEX_PRO('LP_AXIOM', context)
    # ведет на 5 Ж версию
    message_text, keyboard, picture_path = Make_Block('LP_AXIOM')
    message_text = message_text.format(axi0_url = AXIOM_URL)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context)

async def TEST_HOMEJOB(context: ContextTypes.DEFAULT_TYPE):
    day = Get_User_Day(context)
    # wday = get_uwork()
    taskflags = Check_user_flags(day)   # получили taskflags через ДЕНЬ
    uf_ALL_fin = Is_ALL_fin(day, taskflags)   # получили uf_ALL_fin через ДЕНЬ + taskflags
 
    dole_FP = Get_DOLE_FP()        # получили защелку
    print ('>>>>>>>>>>> dole_FP=', dole_FP)
    subflag = False
    if uf_ALL_fin:      # если 3 домашки готово        
        if not dole_FP:    # И если ЕЩЕ НЕ НАЧИСЛЯЛИ нет защелки
            subflag = True
            await FILL_DAY(context)    # поздравления
            await INC_DOLE(context)    # увеличили долю + получили 1 пас
            Set_DOLE_FP(True)          # ставим защелку
            await Adelay(1)
        
        
        week = get_uweek()
        if await WEEK_SHOW(week, context):  subflag = True
        
        if subflag:
            return False 

    return True # need come to START

        
async def TEST_EVENING(context: ContextTypes.DEFAULT_TYPE):
    # wday = get_uwork()
    # doles = get_credos(4)
    day = Get_User_Day(context)         # читаем day    
    taskflags = Check_user_flags(day)   # получили taskflags через ДЕНЬ
    uf_ANY_fin = Is_ANY_fin(day, taskflags)   # получили uf_ALL_fin через ДЕНЬ + taskflags
    uf_ALL_fin = Is_ALL_fin(day, taskflags)   # получили uf_ALL_fin через ДЕНЬ + taskflags
    message = ">🧑🏻‍🎓> Проверка домашнего задания:"  
    mesfin = "\n💤 НАЧАТЬ НОВЫЙ ДЕНЬ ▶️ /start"
    if uf_ALL_fin:       # если 3 домашки готово
        await Inc_Day(context)
        print("Был переход дня")
        Set_DOLE_FP(False)   
        print("Обновлен триггер ДОЛИ")
        warn = f'{message} OK ✅\nВсе задания выполнены, происходит прогресс дня{mesfin}'
        # await SEX(warn, context) 
        await START_AGAIN(warn, context.update, context)
        return True  
    if uf_ANY_fin:       # если 1 домашки готово
        warn = f'{message} OK ☑️\nНе все задания выполнены, нет прогресса марафона {mesfin}'
        # await SEX(warn, context) 
        await START_AGAIN(warn, context.update, context)        
        # Set_DOLE_FP(False)
        # print("Обновлен триггер ДОЛИ")        
        return False
        
    LIVES = get_credos(1)
    if LIVES>0:    # но не в минус
        LIVES -= 1  # сжигание 1 ЖИЗНИ
    save_credos(1, LIVES)
    await SEX(f'{message} НЕ ВЫПОЛНЕНО ❌\n- Вы теряете 1❤️, осталось: {LIVES}❤️ {mesfin}', context)
    if LIVES<=0:
        await END_book(context)
        return False
    
    
async def WEEKJOB(context: ContextTypes.DEFAULT_TYPE):     
    await Inc_Lives(context, lives=1)
    await Inc_Vitas(context, vitas=1)
    # await WEEK_SHOW(week, context)
    await SEX('НЕДЕЛЬНЫЙ ОТЧЕТ: награды получены, ждем ответ от Фрейи', context)
    await FREYA_WEEK(context)
    week = get_uweek()
    save_uweek(week+1)
    await TEST_MONTH(context)
    return
    
    
async def TEST_MONTH(context: ContextTypes.DEFAULT_TYPE):    
    day = Get_User_Day(context)
    if day==MAX_DAYS:        
        # day = 1
        user_progress()   
        await Inc_Lives(context, lives=5)
        await Inc_Vitas(context, vitas=10)
        # if IsUserPREM():
            # pays = IsPREM()
            # tar_bonus = GET_BONS(pays)
            # await Inc_Vitas(context, vitas=tar_bonus)
    if day>MAX_DAYS:
        day = 1  
        save_day(day)        
    # save_credos(4, work)  # дополнительный дубль
    # save_uwork(work) 
    # save_day(day)    
    
    
    
    
async def INC_DOLE(context: ContextTypes.DEFAULT_TYPE):    
    # доля
    dole = get_credos(4)   
    dole += 1 # инкременация 
    if dole==7:  await WEEKJOB(context)
    if dole>7:
        dole = 1
    save_credos(4, dole)
    


# async def INC_WORK(context: ContextTypes.DEFAULT_TYPE):    

    # work = get_uwork()
    # work += 1 # инкременация     

    # if work==MAX_DAYS:        
        # work = 1
        # user_progress()   
        # await Inc_Lives(context, lives=5)
        # await Inc_Vitas(context, vitas=10)
        # """ if IsUserPREM():
        # """     pays = IsPREM()
        # """     tar_bonus = GET_BONS(pays)
       # """      await Inc_Vitas(context, vitas=tar_bonus)
    # if work>MAX_DAYS:
        # work = 1     
    # save_uwork(work)  
   
    
    
async def WEEK_SHOW(week:int, context: ContextTypes.DEFAULT_TYPE): 
    if week==1:
        return await Promo_Show(context)
    if week==2:
        return await Promo_Donna(context)       
            
async def Promo_Show(context: ContextTypes.DEFAULT_TYPE): 
    show_FP = Get_SHOW_FP()
    if not show_FP:        
        await MORE_BONUS(context)   # показать блок Донна
        Set_SHOW_FP(True)     # Донна-пас да=True уже начисляли? да
        return True
    return False   
    
    
async def Promo_Donna(context: ContextTypes.DEFAULT_TYPE): 
    donna_FP = Get_DONNA_FP()
    if not donna_FP:        
        await DONNA(context)   # показать блок Донна
        Set_DONNA_FP(True)     # Донна-пас да=True уже начисляли? да
        return True
    return False
        
    

                







async def MORE_BONUS(context: ContextTypes.DEFAULT_TYPE):
    await SEX_PRO('MORE_BONUS', context)


async def MORE_INFO(context: ContextTypes.DEFAULT_TYPE):
    await SEX_PRO('MORE_INFO', context)







async def Send_Task_Buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TASKS
    # day = Get_Var ('day', context)
    day = Get_User_Day(context)
    # wday = get_uwork()
    taskflags = Check_user_flags(day)
    uf_ALL_fin = Is_ALL_fin(day, taskflags)
    uf_ANY_fin = Is_ANY_fin(day, taskflags)
    buttons = []
    # global TASKS
    # wday = Get_Var('day', context)
    # maxy = N_TAX    # Getask_day(wday)
    
    
    
    
    for i, task in enumerate(TASKS):
        if (i<N_TAX):
            textbut = f"{task}"
            # if i==1:
                # Spec_Task = get_question(day) if day<MAX_DAYS else None
                # if Spec_Task: textbut = Spec_Task 
                
            if taskflags[i]:
                textbut = textbut + " ✅"
            callback = f"hometask_{i}"
            buttons.append([InlineKeyboardButton(textbut, callback_data=callback)])
    textback = "Выйти"
    buttons.append([InlineKeyboardButton(textback, callback_data='start_new')])
    return Make_KEYB(buttons)   
    
    
    
    
async def Ask_TZ(update: Update, context: ContextTypes.DEFAULT_TYPE):
    Set_Var('mid_Ask_Zone', None, context)
    Update_step(13, context)
    await Ask_ZONE(context)    
    
      
    
    
    
async def SEX_PRO(block_name, context: ContextTypes.DEFAULT_TYPE):
    # message_text, keyboard, picture_path = Make_Block(block_name)
    Block_PAK = Make_Block(block_name)
    return await SEX_PROD(Block_PAK, context)
    
    

async def SEX_PROD(block_pak, context: ContextTypes.DEFAULT_TYPE, diw:bool = False):
    message_text, keyboard, picture_path = block_pak
    form = 'BL' if diw else 'B'
    if picture_path:
        print ("SEX_PROD: Найдена фотка, отправляем фото-блок c меню")
        with open(picture_path, 'rb') as photo:
            return await SEX(message_text, context, DOC = photo, MENU = keyboard, FORMAT = form)
    else:
        print ("SEX_PROD: Фотка не найдена, отправляем текст c меню")
        return await SEX(message_text, context, MENU = keyboard, FORMAT = form)


def INIT_VARS (pub, mtype, demo):
    global PUB, MOD_TYPE, DEMO
    PUB = pub
    MOD_TYPE = mtype
    DEMO = demo

def Re_Init(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Re_Init> ")
    user_data = update.effective_user               # получаем Данные юзера
    user_id = update.effective_chat.id              # получаем ИД юзера

    Set_Var ('cur_task', 0, context)             # обнуление индекса задач
    Set_Var ('user_id', user_id, context)       # сохраняем ИД юзера
    # Set_Var('LIFE_HIST_file', LIFE_HIST_file, context)      # сохраняем файл истории
    SUP_CHAT_id = LIFE_CHAT_id if PUB else DEV_CHAT_id
    Set_Var('SUP_CHAT_id', SUP_CHAT_id, context)
    Update_step(0, context)                     # сброшен шаг на нулевой 0
    userfolder = user_id          # если нет имени то прописываем айди как папку
    user_path1, user_path2 = Create_user_folders(MODERATOR_DIR, userfolder)  #  юзер-папки
    Set_Var ('DATA_PATH', user_path1, context)# сохраняем юзер-папку общую
    Set_Var ('user_path', user_path2, context)# сохраняем юзер-папку юзерa
    print(f"M> ТЕКУЩИЙ mod_type: -{MOD_TYPE}- 💪 ")
    if (MOD_TYPE==0):
        Moderator_ID = user_id
    else:
        len_mod = len(MODERATORS)
        # print(f"M> len(MODERATORS) = {len_mod}")
        mod_id = len_mod if MOD_TYPE > len_mod else MOD_TYPE - 1
        Moderator_ID = MODERATORS[mod_id]
        Moderator_Name = Find_User_Name(Moderator_ID)
    if Moderator_Name is None:
        Moderator_Name = Get_Var('user_nick', context)
    print(f"M>>> ПРИНЯТ МОДЕРАТОР: {Moderator_Name}:{Moderator_ID} 💪")
    Set_Var ('MOD_ID', Moderator_ID, context)  # сохраняем
    Set_Var ('MOD_NAME', Moderator_Name, context)# сохраняем
    Set_Var ('mid_Start_Rules', None, context)  # обнуление
    Set_Var ('mid_Start_Rumod', None, context)  # обнуление 
    # Set_Var ('DEMO', DEMO, context)  # default 1v
    Set_Var ('SERVER_TZ', get_server_timezone(), context)   # default +3
    Check_USER_Rang(context)

# async def SEX_PRO2(block_name, forma, context: ContextTypes.DEFAULT_TYPE):
    # message_text, keyboard, picture_path = Make_Block(block_name)
    # message_text, keyboard, picture_path = Make_Block(block_name)
    # message_text = message_text.format(forma)
    # Block_PAK = message_text, keyboard, picture_path
    # await SEX_PROD(Block_PAK, context) 


async def After_Init(context: ContextTypes.DEFAULT_TYPE):
# проверяем Рефера и как запущен Юзер-Клиент    
    Refer_ID = await Check_Referrals(context)
    if Refer_ID:
        text = f"Замечательно 🍕 Вы пришли по реферальной ссылке от {Refer_ID}"
        await SEX(text, context)
    else:
        err_result = Get_VAR('reff_run_info', "нет реферальных таблиц", context)
        text = "🍕ДСЗ🍕 > " + err_result
    print (text)
# затем проверяем своих Рефералов и статистику
    await Check_User_Refdata(context)
# если TESTER - выводим Отладку в 1 блоке
    # if REV: # TESTER
        # print("ПЕРВИЧНАЯ ОТЛАДКА >>> ",end='')
        # await debug_user_data(False, context)
# подстраховка ответов
    print ("подстраховка ответов: ", end='')
    if not Get_day_responses(1):
        print ("нет ответов > разметка шаблона")
        Init_Answers()
    else:
        print ("есть ответы")
    Set_Var ('mid_Start_Rules', None, context)  # обнуление 
    # Set_Var ('mid_Start_Rumod', None, context)  # обнуление    
# проверяем 1й раз (целкостность) Юзера
    # if Get_Var('uf_IsNew', context):



 
async def Ask_ZONE(context: ContextTypes.DEFAULT_TYPE):
    textzone, keybzone, picture = FORM_ZONE(context)
    # textzone = Text = TextBrand('timezone_bold')
    mid_Ask_Zone = Get_Var('mid_Ask_Zone', context)
    if picture:
        print ("Ask_ZONE: Найдена фотка, отправляем фото-блок c меню")
        photo =  open(picture, 'rb')
            # await SEX(message_text, context,  MENU = keyboard, FORMAT = 'B')   
    else:
        print ("Ask_ZONE: Фотка не найдена, отправляем текст c меню")
        photo = None
        # await SEX(message_text, context, MENU = keyboard, FORMAT = 'B')
    
    # if mid_Ask_Zone:

        # await SEX(textzone, context, EDIT=mid_Ask_Zone, FORMAT='B', MENU=keybzone, DOC = photo)

    # else:
    message = await SEX(textzone, context, MENU=keybzone, FORMAT='B', DOC = photo)
    Set_Var('mid_Ask_Zone', message.message_id, context)    

        
async def AskTZ_CALLBACK(choice, update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query
    
    choice = choice[1:]
    if choice == "final":
        Update_step(19, context)
        print("ВЫХОДИМ!!!")
        client_utc = Get_Var('user_utc', context)
        AskText = f"🌐 Выбрана TIMEZONE ✅ {client_utc}"
        if AskText:
            await SEX(AskText, context)
        await POST_PREP(update, context)
        return
    
    # Handle timezone selection
    if choice == "utc":
        Update_User_ZONE(0, context)
    else:
        tz = TIMEZONES.get(choice)
        if tz is not None:
            Update_User_ZONE(int(tz), context)
    
    # Get the message ID from context or query
    mid_Ask_Zone = Get_Var('mid_Ask_Zone', context)
    if not mid_Ask_Zone and query.message:
        mid_Ask_Zone = query.message.message_id
        Set_Var('mid_Ask_Zone', mid_Ask_Zone, context)
    
    # Use SEX with EDIT parameter to update the existing message
    if mid_Ask_Zone:
        textzone, keybzone, picture = FORM_ZONE(context)
        photo = open(picture, 'rb') if picture else None
        try:
            await SEX(
                textzone, 
                context, 
                EDIT=mid_Ask_Zone, 
                FORMAT='B', 
                MENU=keybzone, 
                DOC=photo
            )
        finally:
            if photo:
                photo.close()


def FORM_ZONE(context: ContextTypes.DEFAULT_TYPE):
    # Text = TextBrand('timezone_bold')
    Text, _ , picture = Make_Block('JOIN4')
   
    # Text = message_text
    client_offset = Get_Var('user_tz', context)
    utc_str = Get_Var('user_utc', context)
    client_time = get_client_time()
    client_str = T2STR(client_time)
    midco = '🌐' if client_offset==0 else '✅' 
    zoner = f"Пояс {utc_str} {midco} Время {client_str[:-3]}"
    hour = client_time.hour
    hour_index = hour if hour != 0 else 12  # Индекс для иконки (1-12)
    circle = chrono_clock[hour_index - 1]  # Получаем иконку # ⏰
    timer_ok = f"{circle} ПРИНЯТЬ ☑️"
    button_ZONE = InlineKeyboardButton(zoner, callback_data='🌐utc')
    button_OK = InlineKeyboardButton(timer_ok, callback_data='🌐final')
    buttons = []
    buttons.append([button_ZONE])
    for timezone, offset in TIMEZONES.items():
        textzone = timezone
        if offset==client_offset:          # если заходили - отметка
            textzone+=" ✅"
        buttons.append([InlineKeyboardButton(textzone, callback_data=f'🌐{timezone}')])
    buttons.append([button_OK])
    keyb_time = Make_KEYB(buttons)
    return Text, keyb_time, picture
  



async def Job_TASK(tindex, update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TASKS
    task = TASKS[tindex]
    Set_Var('cur_task', tindex, context)
    chat_id = Get_Uid(context)
    day = Get_User_Day(context)
    # wday = get_uwork()
    
    print(f"> Выбрано домашнее задание: {tindex}:{task} (день {day})")
    response = Get_task_response(tindex, day)
    
    if tindex==2 and day<MAX_DAYS:  Spec_Task = get_question(day)
    
    if response: # Если ответ есть то ПРАВКА
        print(f"Вывод ответа: {response}")
        text = f"✅ *Ваш ответ* {task} 👉🏻\n`{response}`"  
        if tindex==2:
            # Spec_Task = get_question(day)
            special = f"✅ *Вопрос Дня* ❓ _{Spec_Task}_\n" if Spec_Task else ''
            text = f"{special}{text}"
                    
        
        button1 = InlineKeyboardButton("✍️ Редактировать", callback_data='edit_name')
        button2 = InlineKeyboardButton("📚 ОБРАТНО", callback_data='start_day')
        buttons  = [[button1],[button2]]
        keyb4 = Make_KEYB(buttons)
        if update.effective_message:
            await update.effective_message.reply_text(text, reply_markup=keyb4, parse_mode="Markdown")
    else:
        Update_step(5, context)
        print(f"Ожидается ввод ответа: {task}")
        text=f"Введите в чат свой ответ на задание {task} 👇🏻"
        
        if tindex==2 and day<MAX_DAYS:
            # Spec_Task = get_question(day)
            if Spec_Task: 
                print(f"Специальный вопрос: _{Spec_Task}_")
                text = f"Введите в чате ответ на *вопрос дня:*\n{Spec_Task} 👇🏻"        
                
        if update.effective_message:
            await update.effective_message.reply_text(
            text=text,
            parse_mode="Markdown"  # Включаем поддержку MarkdownV2
        )

async def update_Answer(msg: str, context: ContextTypes.DEFAULT_TYPE):
    print("Записываем в БАЗУ через Update_task_response > ")
    uid = Get_Uid(context)
    day = Get_User_Day(context)
    # day = Get_Var('day', context)
    # wday = get_uwork()
    task_index = Get_Var('cur_task', context)
    togo = f"Отладка перед 🔋 update_Answer: day={day} id={uid} Tindex={task_index}"
    print(togo)
    # togo = f"Отладка перед 🔋 update_Answer: msg={msg}"
    # print(togo)
    Update_task_response(task_index, day, msg)
    text = "Ваш ответ успешно записан в базу 🔋"
    await SEX(text, context)
    text = "Проверяем... ⌛ "
    sent = await SEX(text, context)
    response = Get_task_response(task_index, day) #
    if response:
        print(f"ОТВЕТ: {response}")
        # await context.bot.edit_message_text(chat_id=uid, message_id=sent.message_id, text=text+response)
        await SEX(text+response, context, EDIT=sent.message_id)
        return response
    else:
        print("Ответ не записан ОШИПКА Ф Update_task_response")
        return None

async def UPDATE_ANSWER(msg: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    response = await update_Answer(msg, context)
    if response:
        Update_step(4, context)
        if await TEST_HOMEJOB(context):
            await START_DAY(update, context)
            
    else:
        print("Ответ не записан, рестарт")
        await SEX("Ответ не записан, Видимо зависла База Данных...", context)
        context.user_data['last_err'] = "зависла База Данных"
        # await Err_ACTOR(update, context)


def Is_ALL_fin(day, flags) -> bool:
    maxy = Getask_day(day)
    limited_flags = flags[:maxy]
    ALL_Tasx = all(limited_flags)  # Собирает все флаги по методу AND)
    print(f"Домашка - все готовы? > {ALL_Tasx}")
    return ALL_Tasx

def Is_ANY_fin(day, flags) -> bool:
    maxy = Getask_day(day)
    limited_flags = flags[:maxy]
    ANY_Tasx = any(limited_flags)  # Собирает все флаги по методу OR
    print(f"Домашка - хоть один готов? > {ANY_Tasx}")
    return ANY_Tasx
    
def Is_AFK(day, flags):
    maxy = Getask_day(day)
    limited_flags = flags[:maxy]
    N_Tasx = sum(limited_flags)  # Собирает все флаги по методу OR
    print(f"Домашка - сколько готово? > {N_Tasx}")
    return N_Tasx    
    
    

async def ALLOW(context: ContextTypes.DEFAULT_TYPE):
    if SU:
        dev_name = Get_Var('dev_name', context)
        print (">{dev_name} > ДОСТУП ОДОБРЕН")
        return True
    else:
        await SEX("❌ У Вас нет прав 🙅🏼 Ревизора 🙋🏼 для этой команды", context)
        return False

async def ALLOWED(context: ContextTypes.DEFAULT_TYPE):
    if ADM:
        dev_name = Get_Var('dev_name', context)
        print (f">{dev_name} > ДОСТУП ОДОБРЕН")
        return True
    else:
        await SEX("❌ У Вас нет прав 🙅🏼 Администратора 🦹🏼 для этой команды", context)
        return False

async def ALLOW_DEV(context: ContextTypes.DEFAULT_TYPE):
    if DEV:
        dev_name = Get_Var('dev_name', context)
        print (f">{dev_name} > ДОСТУП ОДОБРЕН")
        return True
    else:
        await SEX("❌ У Вас нет прав 🙅🏼 Модератора 🎅🏻 для этой команды", context)
        return False

def Check_USER_Rang(context: ContextTypes.DEFAULT_TYPE, user:int = None):
    global SU, REV, ADM, DEV
    user_id = user if user else Get_Uid(context)
    user_rang = 0
    if user_id in REVISORS:
        user_rang = 1
        REV = True
    if user_id in ADMINS:
        user_rang = 2
        ADM = True
    if user_id in MODERATORS:
        user_rang = 3
        DEV = True
    Set_Var('user_rang', user_rang, context)
    rang_str = RANGS[user_rang]
    Set_Var('user_status', rang_str, context)
    SU = user_rang>0
    if SU:
        devname = Find_User_Name(user_id)
        if devname:
            Set_Var('dev_name', devname, context)
        print (f"> Добро пожаловать {devname}, Ваш Ранг:{user_rang}-{rang_str}")
    return user_rang

def Check_user_flags(day):
    log = False
    responses = Get_day_responses(day)
    taskflags = [False] * N_TAX
    if responses is None:
        print("Херня какая-то с днем или ответами, проверь!")
        return taskflags
    if not responses:
        print("Ответов в базе пока нема, долбоёб! 😉")
        return taskflags
    if log:
        print("Задания и ответы пользователя:")
    for i, title in enumerate(TASKS):
        if i < len(responses) and responses[i] is not None:
            if log:
                print(f"{title}: {responses[i]}")
            taskflags[i] = True
        else:
            if log:
                print(f"{title}: -нет-")
    return taskflags


async def UINFO(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if ERRO:
        # await Err_Tesla_Handler(DATA_BASS, update, context)
    await Userfo(context)
    # await MAKE_DAYBUCK('финал', context)


async def Show_TIME(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = FORM_TIME(context)
    uid = Get_Uid(context)
    Set_Var('mid_Ask_Zone', None, context)
    mid_Show_Time = Get_Var('mid_Show_Time', context)
    if mid_Show_Time:  # BOLD
        await delete_user_message(update, context)
        # await ESB(mid_Show_Time, text, context)
        await SEX(text, context, EDIT=mid_Show_Time, FORMAT='B')
    else:
        message = await SEX(text, context, FORMAT='B')
        Set_Var('mid_Show_Time', message.message_id, context)


async def Reset_Sure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(" > Админ - Reset_DELETE")
    # user_id = update.effective_chat.id
    user_id = Get_Uid(context)
    delete_user(user_id)
    Re_Init(update, context) # инициализация
    await START_AGAIN('Учетная запись удалена', update, context)


async def Reset_DELETE(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(" > Админ - Reset_DELETE") 
    await SEX_PRO('RESET_WARN', context) 

async def Reset_RUN(choice, update: Update, context: ContextTypes.DEFAULT_TYPE):
    if choice == '❌clearpro':
        await Clear_PRO(update, context)
        # await START_DAY(update, context)
    if choice == '❌deltasx':
        await Clear_user_TASKS(context)
        await START_DAY(update, context)
    if choice == '❌restart':
        savedb_time(None)
        Set_Var('day', 1, context)
        save_day(1)
        save_uweek(1)
        # save_uwork(1)
        save_credos(4, 0)
        Set_DOLE_FP(False)
        # await Inc_Day(context)  # теперь НЕ вызывает рестарт
        # await Start_DAY(update, context)
        Re_Init(update, context) # инициализация
        await START_AGAIN('Марафон был перезапущен', update, context)
    if choice == '❌deluser':
        await Reset_DELETE(update, context)
    if choice == '❌reset_sure':
        await Reset_Sure(update, context)            
            


async def Reset_TSK(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if not await ALLOWED(context):
        # return        
    print(" > Админ - Reset_TSK")
    # b1=InlineKeyboardButton("🆑 Удалить все ответы", callback_data='❌deltasx')
    # b2=InlineKeyboardButton("⭕️ Перезапустить марафон", callback_data='❌restart')
    # b3=InlineKeyboardButton("🅰️ Аннулировать Премиум", callback_data='❌clearpro')
    # b4=InlineKeyboardButton("❌ Удалить учетную запись", callback_data='❌deluser')
    # b5=InlineKeyboardButton("🔙 Отмена операции", callback_data='back_menu')
    # buttons = [[b1],[b2],[b3],[b4],[b5]]
    # text = "*Выберите нужный пункт* ➡️\n❌ Удалить учетную запись `- удалить учётку Игрока из нашей базы, нужен перезапуск бота`"
    # return await Make_MENB(text, buttons, context)
    await SEX_PRO('RESET_CON', context) 

async def Clear_PRO(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if not await ALLOWED(context):
        # return
    print(" > Админ - Clear_PRO")
    if not IsUserPREM():
        return
    save_pays(0)
    role = get_role()
    if IsUserPreme(role):
        role = role.replace('+', '')
        save_role(role)
    await SEX("Премиум аккаунт был ⭕️ анулирован", context)
    Sdelay(1)
    await START_BOOK(update, context)
        
        
        
async def Prep1_REFO(context: ContextTypes.DEFAULT_TYPE):        
    user_nick = Get_Var ('user_nick', context)
    code = Get_VAR('user_refcode', "нет кода", context)
    link = Get_VAR('user_reflink', "нет ссылки", context)
    hyp_link = f" _копировать ниже_ 👇🏻\n`{link}`"
    ref_count = Get_VAR('ref_count', "0", context)

    message_text, keyboard, picture_path = Make_Block('REFER')
    message_text = message_text.format(
        # donna_url = donna_url, uni_url = uni_url, axi_url = axiom_url,
        name = user_nick, ref_code = code, 
        ref_link = hyp_link, ref_cont = ref_count
         )
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context)

        
async def REFER_FULL(update, context: ContextTypes.DEFAULT_TYPE):    
    print("REFER_FULL: ")    
    user_nick = Get_Var ('user_nick', context)
    donna_url = Get_DONNA_URL()
    uni_url = Get_UNI_URL()
    axiom5life_url = Get_AXI5M_URL()
    axioma_url = AXIOM_URL
    axioma_ref = Get_AXI0M_REF()      
    
    reful_text, keyboard, picture_path = Make_Block('REFER_FULL')
    reful_text = reful_text.format( name = user_nick, 
    donna_url = donna_url, 
    uni_url = uni_url, 
    axi5_url = axiom5life_url,
    axi0_ref = axioma_ref,
    axi0_url = axioma_url,
    )                       
         
    Block_Pk = reful_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context, diw=True)
    


async def Prep2_REFO(context: ContextTypes.DEFAULT_TYPE):       
    ref_data = Get_Refer_Data()
    ref_table = Make_Refer_Table(ref_data)
    ref_stat = '\n'+str(ref_table) if ref_table else "Пока нет структуры"
    Set_Var('user_refstat', ref_stat, context)
    refstata = Form_Port(97, ref_stat) # РЕФ.m 🤝
    # await SEB(refstata, context)
    await SEX(refstata, context, FORMAT='B') 
    return

async def REFER(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await REFER_UPDATE(context)
    await Prep1_REFO(context)
    # Set_Var('mid_Invite', None, context)
    # text, buttons = await Prep1_REFO(context)
    # keyboard = Make_KEYB(buttons)
    # await SEX(text, context, FORMAT='B', MENU=keyboard)
    # await SEFoM('refer_menu', text, keyboard, context)
    # await Scroll_chat_down(update, context) 


async def REFER_INV(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    await REFER_UPDATE(context)
    Update_step(10, context)
    Set_Var('mid_Invite', None, context)
    await SEX_PRO("INVITE_ADDON", context)
    await Adelay(0.2)  
    await REFER_INVITE(context)


async def REFER_INVITE(context: ContextTypes.DEFAULT_TYPE):    
    user_id = Get_Uid(context)
    friend_name = Get_VAR('friend_name', None, context)
    link = Get_VAR('user_reflink', "нет", context)        
    forwho = friend_name.upper() + '!  '  if friend_name else ''
    
    invite, keyboard, picture_path = Make_Block('INVITE')
    invite = invite.format(
         forwho = forwho, ref_link = link )
    Block_Pk = invite, keyboard, picture_path
    
    
    
    
    # invite = TextBlock('invite_msg')
    # invite = invite.format(friend_name=friend_name, BRAND_RUS=BRAND_RUS[1])      
    # invite += link
    # print(invite) 

    message_id = Get_VAR('mid_Invite', None, context)    
    if message_id:   # ANALOG=LASTBLOCK
        await SEX(invite, context, DOC = picture_path, FORMAT='B', EDIT=message_id)
    else:
        message = await SEX_PROD(Block_Pk, context)
        # await SEX(invite, context, DOC = photo) 
        Set_Var('mid_Invite', message.message_id, context)


async def REFER_UPDATE(context: ContextTypes.DEFAULT_TYPE):
    user_id = Get_Uid(context)
    ref_code = get_ref_code()  # 1 читаем из памяти
    # ref_code = Get_Var('user_refcode', context)  # 1 читаем из памяти
    # if not ref_code:
        # ref_code = Get_Var('user_refcode', context)                # 2 читаем из базы д.
    if not ref_code:
        ref_code = Generate_Ref_Code()           # 3 генерируем! + пишем в базу
        await SEX(f"🤝 Персональный реферальный код: {ref_code}", context)
    Set_Var('user_refcode', ref_code, context)   # пишем в память
    link = Get_Var('user_reflink', context)
    if not link:
        # await SEM ("🤝 Генерация реферальной ссылки 🤝", context)
        print ("Генерация реферальной ссылки...")
        link =  Comb_Reflink(ref_code)
        Set_Var('user_reflink', link, context)
    ref_count = get_ref_count()
    Set_Var('ref_count', ref_count, context)
    # direct_referrals, second_referrals, bonus = Calc_Bonus(user_id)
    # print (f"👥 Ваши рефералы: ({ref_count}) - {direct_referrals} - {second_referrals}")
    # if ref_count:
        # Set_Var('ref_count', ref_count, context)
    # if direct_referrals:
        # Set_Var('ref_count1', direct_referrals, context)
    # if second_referrals:
        # Set_Var('ref_count2', second_referrals, context)
    # if bonus:
        # Set_Var('ref_rating', bonus, context)
    return ref_count 





async def REFER_RUN(choice, update, context: ContextTypes.DEFAULT_TYPE):
    # user_id = Get_Uid(context)
    print("Обработчик REFER_RUN: ", choice)    
    if choice == '🤝stata':  #  обновить реф-инфу
        await REFER_UPDATE(context)  
        await REFER(update, context)    
    elif choice == '🤝invite':  # пригласительное сообщение 
        await REFER_INV(update, context)
        # Update_step(10, context)
        # await REFER_INVITE(context)
        # await MAKE_REFBACK(context)
    elif choice == '🤝table':  # расширеная таблица
        await Prep2_REFO(context)
        # await User_INFO(update, context)
        # await MAKE_REFBACK(context)
    elif choice == '🤝partner':  # расширеная таблица
        await REFER_FULL(update, context)        
        # await Prep2_REFO(context)
        # await User_INFO(update, context)
    elif choice == '🤝donna_set': # --NEW!!!          
        await DONNA_SET(update, context) 
    elif choice == '🤝uni_set': # --NEW!!!          
        await UNI_SET(update, context)         
    elif choice == '🤝axi0_set': # --NEW!!!          
        await AXI0_SET(update, context) 
    elif choice == '🤝axi5_set': # --NEW!!!          
        await AXI5_SET(update, context)          
        

def FORM_TIME(context: ContextTypes.DEFAULT_TYPE):
    server_time, client_time = get_time()
    now1 = Show_Time_Info(server_time)
    now2 = Show_Time_Info(client_time)
    now3 = T2STR(client_time)
    hour = client_time.hour
    hour_index = hour if hour != 0 else 12  # Индекс для иконки (1-12)
    circle = chrono_clock[hour_index - 1]  # Получаем иконку
    icoh = icons[int(hour/2)]
    ico1 = random.choice(icons)
    ico2 = icons[random.randrange(5)]  # len(icons)
    # ico3 = icons[random.randint(0, 4)] # len(icons) - 1
    SERVER_TZ = str(Get_Var ('SERVER_TZ', context))
    user_utc = str(Get_Var ('user_utc', context))
    stp = Get_VAR ('stepper', 0, context)
    stp +=1
    sts = stp*"."
    Set_Var('stepper', stp, context)
    static = " (статика)" if stp<40 else ""
# user_tz = str(Get_Var ('user_tz', context))
    div = " "   # ================
    head = f"⚜️ *АГЕНТ* 👁 *СЛЕЖКИ* {ico1} *ВРЕМЕНИ*"
    t_sz = f"🌍 *SERVER TIMEZONE* > 🌒 *{SERVER_TZ}*"
    t_st = f"🌞 *SERVER TIME* > ⌛️ *{now1}*"
    ser_blok = "\n".join([div, t_sz, t_st, div])
    t_cz = f"🌐 *ВАШ ЧАСОВОЙ ПОЯС* > *{user_utc}*"
    t_ct = f"🕒 *ВАШЕ ВРЕМЯ* > *{now2}*"
    cli_blok = "\n".join([t_cz, t_ct])
    timer = f"{sts}{icoh} *ЧАСЫ* <{circle}> *{now3}* {static}"
    t_chk = f"{ico2} */time* 👉🏻 Проверить ВРЕМЯ"
    hed = "\n".join([head, div])
    if SU:
        hed += ser_blok
    med = "\n".join([hed, cli_blok, div, timer, t_chk])
    t_set = "🌐 */timezone* 👉🏻 Задать часовой пояс"
    t_ext = "🕰 */begin* 👉🏻 Выйти в меню ДНЯ"
    fin = "\n".join([t_set, t_ext]) # ================
    if SU:                          # =SU=ADDON=======
        ta1 = "❓ */help* 👉🏻 Помощь"
        ta2 = "🧩 */debug* 👉🏻 Отладка"
        ta3 = "♻️ */start* 👉🏻 Рестарт бота"
        tadm = "\n".join([ta1, ta2, ta3])
        fin += "\n"+tadm
    output_message = "\n".join([med, div, fin])
    return output_message



async def Debug_UD(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ALLOW(context):
        return
    print("> Админ - Вывести список переменных:")
    await debug_user_data(True, context)

def Err_Detailer(context: ContextTypes.DEFAULT_TYPE):
 # Получаем информацию об ошибке
    error = context.error
    error_type = type(error).__name__
    error_message = str(error)
# Получаем трассировку стека
    tb = traceback.extract_tb(sys.exc_info()[2])
# Находим последний элемент трассировки из вашего кода
    project_dir = '.'
    last_call = None
    for call in reversed(tb):
        if project_dir in call.filename:
            last_call = call
            break
    if last_call:
        filename = os.path.basename(last_call.filename)
        line_no = last_call.lineno
        func_name = last_call.name
        line = last_call.line
    else:
        filename = "Unknown"
        line_no = "Unknown"
        func_name = "Unknown"
        line = "Unknown"
# Формируем подробное сообщение об ошибке
    error_details = f"""
Произошла ОШИБКА: {error_type}
Файл: {filename}, Строка: {line_no}, Функция: {func_name}
Код: {line}
Колбэк: {error_message}

Трассировка стека:
{traceback.format_exc()}
    """
    NT_FLAG = 'NoneType' in error_message
    return NT_FLAG, error_type, error_details

def Show_time_ingame(context: ContextTypes.DEFAULT_TYPE):
    user_stime = Get_Var('user_stime', context)
    if user_stime:
        user_time = Show_Game_Time(user_stime)
        Set_Var('user_time', user_time, context)
        return user_time
    else:
        return None

async def Check_User_Refdata(context: ContextTypes.DEFAULT_TYPE):
    referals = await REFER_UPDATE(context)
    # ref_code = get_ref_code()
    # if not ref_code:
        # Regen_Link(context)
    # else:
        # Set_Var("user_refcode", ref_code, context)
    print(f"Check_User_Refdata >OK> ref.cnt > {referals}")
    return referals

async def Check_Referrals(context: ContextTypes.DEFAULT_TYPE):
    start_parameter = Get_Var('start_param', context)  # забираем Ключ
    if start_parameter:
        reff_run_info = Process_Relink(start_parameter)
        if reff_run_info['success']:
            print ("Вывожу итоги проверки рефералов >")
            print (reff_run_info)
            refers_count = reff_run_info['referral_count']
            referrer_id = reff_run_info['referrer_id']
            referrer_lives = reff_run_info['lives']
# Настройка АФИЛИАТОВ           
            Donna_url = read4db('user_donna_url', sender = referrer_id)
            Set_DONNA_URL(Donna_url)          
            Uni_url = read4db('user_uni_url', sender = referrer_id)
            Set_UNI_URL(Uni_url)
            Axi0_ref = read4db('user_axi0_url', sender = referrer_id)
            Set_AXI0M_REF(Axi0_ref)          
            Axi5_url = read4db('user_axi5_url', sender = referrer_id)
            Set_AXI5M_URL(Axi5_url)             

# Отправляем уведомление реферу
            name = Get_Var('user_nick', context)
            text=f"ПОЗДРАВЛЯЮ! 💪 По Вашей ссылке 🤝\nприсоединился новый пользователь: {name}\nВаше общее число рефералов: {refers_count}"
            await SEX(text, context, SENDER = referrer_id)
# Начисляем бонус рефереру
            await Inc_ref_Lives(referrer_id, 1, context)
            return referrer_id
        else:
            Set_Var("reff_run_info", reff_run_info['error'], context)
            return None
    else:
        # reff_run_info = {'success': False, 'error': 'Нету аргумента старта, бот запущен обычным образом'}
        Set_Var("reff_run_info", "Нет аргумента старта, тривиальный запуск", context)
        return None

def Make_Refer_Table(data):
    report = ""
    for referral in data:
        user_id = referral[0]
        user_name = ESU(referral[1]) # оборачка Нейма Юзера
        n2cnt = referral[2]
        dtime_str = shot(referral[3]) # удаляем миллисекунды и зону
        report += f"=====================================\n"
        report += f"👤{user_name} 🆔:{user_id}\n"
        report += f"Дата регистрации: {dtime_str}\n"
        report += f"Число 2ур. рефералов: {n2cnt}\n"
    return report


async def debug_user_data(log, context: ContextTypes.DEFAULT_TYPE):
    print(">> Отладка context.user_data:")
    debug_message = "Отладка context.user_data:\n"
    for key, value in context.user_data.items():
        debug_message += f"{key}: {value}\n"
        print(f"{key}: {value}")
    if log:
        await SEX(debug_message, context, FORMAT='L')
        await MAKE_DAYBACK(context)
        await Scroll_chat_down(context.update, context)

def Find_User_Name(uid):
    if not isinstance(uid, int):
        uid = int(uid)
    for name, user_id in DEVELOPERS.items():
        if uid == user_id:
            return name
    return None  # Return None if user ID is not found in the dictionary



def TextBrand(title, index=0) -> str:
    text = TextBlock(title)
    if text:
        text = text.format(BRAND_RUS=BRAND_RUS[index])
    return text

#               --------HNDLRS-------------
async def VIDEO_RUN(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = None
    video:Video = update.message.video
    if video:
        file = await context.bot.get_file(video.file_id)
        file_id = file.file_unique_id
        print("Пришло круглое видео: ", file_id)
    if file:
        await UMR("Ваше видео записано 🎥", update)
        text = "Юзер записал ВИДЕО: " + str(file_id)
        if await UPDATE_ANSWER(text, update, context):
            print("Кругляш записан в базу")
        else:
            print("Ошибка записи Кругляша в БД")
            await UMR("Ошибка при записи ВИДЕО в базу", update)

async def AUDIO_RUN(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = None
    audio: Audio = update.message.audio
    voice: Voice = update.message.voice
    if audio:
        file = await context.bot.get_file(audio.file_id)
        print(f"Пришло аудио сообщение ({file.file_unique_id})")
    elif voice:
        file = await context.bot.get_file(voice.file_id)
        print(f"Пришло голосовое сообщение ({file.file_unique_id})")
    await UMR("Ожидайте распознавания 🗣", update)
    if file: # Преобразование аудио в текст
        text = await Transcribe_audio(file, context)
        if "err:" in text:  # Проверка результата на наличие ошибки
            print("Обнаружена ошибка:", text)
        else:
            print(f"Текст аудио получен: ({text})")
            await UMR(f"Вы сказали: 🗣 {text}", update)
            if await UPDATE_ANSWER(text, update, context):
                print("Ответ был распознан и записан в базу")
            else:
                print("Ошибка UPDATE_ANSWER записи ответа в базу")
                # await UMR("У нас ошибка при распознании аудио", update)


async def INPUT_RUN(msg, update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CAPS
    step = Get_Var('step', context)
    chat_id = Get_Uid(context)
    # Set_Var ('user_id', chat_id, context)
    print(f"= Пришло сообщение ОТ={chat_id} ввода на ШАГЕ={step} ... > ", end='')
    print(f" {msg}")
    if (step==1):       # Stage step=1 - register - input NAME
        await START_JOIN2_GOT(msg, update, context)
    if (step==5):       # stage 5 input HOME JOB TASK
        return await UPDATE_ANSWER(msg, update, context)
    # if (step==6):       # stage 6 input DAY
        # context.args = [msg]
        # return await Set_DAY(update, context)
    if (step==8):       # stage 8       MODERATOR input REFUSE
        await Mod_Up_Refuse (msg, context)  # save refuse answer to db
        Update_step(19, context) # last silence Step
        # Send_STICKER("нет-нет", context)    #  тупой банан
        return f"Временная зона '{msg}' неясна, лучше введите часовой пояс"
        await UMR("Ваш отказ отправлен Игроку", update)
    if (step==7):       # stage 9       FEED input BUG-REPORT
        print("игнорим Заход в BugSpy_Handler по Step=7")
        # await BugSpy_Handler(msg, context)
        return
    if (step==10):       # stage 10       REFER input Friend Name
        print(" > Вводим имя друга")
        Set_Var("friend_name", msg, context)
        await delete_user_message(update, context)
        return await REFER_INVITE(context)  # Вызываем REFER_INVITE повторно
    if (step==11):       # stage 11       DONNA
        print(" > Вводим ссылку на Донну")
        seek = '/donnaaibot'
        htps = 'https://'
        Update_step(19, context) # last silence Step
        if seek in msg: 
            if not msg.startswith(htps):
                msg = htps + msg
            Set_DONNA_URL(msg)
            await delete_user_message(update, context)
            await SEX('*Ссылка проекта Донна успешно установлена* ✅', context, FORMAT='B')
        else:
            await SEX('▶️ *Неверная ссылка Донна* ⛔️ *Отмена ввода*', context, FORMAT='B')
        return await REFER_FULL(update, context) 
        # Update_step(19, context) # last silence Step
 

    if (step==12):       # stage 12       MOD_CON enter user N=Id
        print(" > Вводим номер юзера в БД")
        max_id = int(Get_VAR('users_count', 1, context))
        if msg.isdigit():
            uid = int(msg)
            if 1 <= uid <= max_id:
                Set_Var('mod_unid', uid, context)
                print(" > Номер Юзера в БД", uid)
                # Update_step(19, context)
                # CAPS = []
                return await MOD_CON(context)
        error_message = f"Пожалуйста, введите целое число от 1 до {max_id}."
        await delete_user_message(update, context)
        return await SEX(error_message, context)
    if (step==13):       # stage 13       enter user TimeZone
        print(" > Ручной ввод TimeZone")
        if msg.isdigit() or ((msg.startswith('-') or msg.startswith('+')) and msg[1:].isdigit()):
            utc_offset = int(msg)
            if -12 <= utc_offset <= 14:
                Update_User_ZONE(utc_offset, context)
                await Ask_ZONE(context)
            else:
                await UMR("Ошибка: Введите корректное значение часового пояса от -12 до +14", update)
        else:
            await UMR(f"Временная зона '{msg}' неясна, лучше введите часовой пояс", update)
    if (step==14):       # stage 14       enter time CRON edit TASK
        print(" > Ручной ввод КРОН-ЗАДАЧА>ПРАВИТЬ>ВВОД>ВРЕМЯ")
        Update_step(19, context)
        return await Crons_Edit(msg, context)
    if (step==15):       # stage 15       enter CRON add TASK
        print(" > Ручной ввод КРОН-ЗАДАЧА>ДОБАВИТЬ>ВВОД>ИМЯ-ВРЕМЯ")
        Update_step(19, context)
        return await Crons_Add_New(msg, context)
    if (step==16):       # stage 16       MOD_CON enter PM to user
        print(" > Вводим послание для Юзера")
        # Update_step(12, context)
        user_uid = Get_Var('mod_uid', context)
        await SEX("Ваше сообщение успешно выслано", context)
        await SEX(msg, context, SENDER = user_uid)
        return await MOD_CON(context)
    if (step==17):       # stage 17   MIG_RUN  enter argument=filename
        print(" > Вводим аргумент для миграции")
        context.args = [msg]
        return await MIG_RUN(update, context)        
    if (step==18):       # stage 18       UNNI
        print(" > Вводим ссылку на UniLIVE")
        seek = 'h.juhetec.com/'        
        htps = 'https://'
        Update_step(19, context) # last silence Step
        if seek in msg: 
            if not msg.startswith(htps):  msg = htps + msg
            Set_UNI_URL(msg)
            await delete_user_message(update, context)
            await SEX('*Ссылка проекта UniLIVE успешно установлена* ✅', context, FORMAT='B')
        else:
            await SEX('▶️ *Неверная ссылка UniLIVE* ⛔️ *Отмена ввода*', context, FORMAT='B')
        return await REFER_FULL(update, context) 
        # Update_step(19, context) # last silence Step        
    # if (step==19):       # stage 19 pass sismilaer ste0  
        # await delete_user_message(update, context)
        # print(" Было удалено как мусор")        
    if (step==20):       # stage 20       enter user uwork
        print(" > Ручной ввод cheat")
        return await FREYA_PUSH(msg, update, context)
    if (step==21):       # stage 21      AXIOM
        print(" > Вводим логин на AXIOMA")
        # seek = 'axioma'
        htps = 'https://'
        Update_step(19, context) # last silence Step
        if len(msg)>3 and len(msg)<32: 
            # if not msg.startswith(htps):  msg = htps + msg
            
            Set_AXI0M_REF(msg)
            await delete_user_message(update, context)
            await SEX('*Логин проекта AXIOMA успешно установлен* ✅', context, FORMAT='B')
        else:
            await SEX('▶️ *Неверный логин AXIOMA* ⛔️ *Отмена ввода*', context, FORMAT='B')
        return await REFER_FULL(update, context)
        
    if (step==22):       # stage 22       AXI 5 life
        print(" > Вводим ссылку на AXI 5 life")
        seek = '/five_live_axioma_bot'
        htps = 'https://'
        Update_step(19, context) # last silence Step
        if seek in msg: 
            if not msg.startswith(htps):  msg = htps + msg
            Set_AXI5M_URL(msg)
            await delete_user_message(update, context)
            await SEX('*Ссылка проекта 5LIFE успешно установлена* ✅', context, FORMAT='B')
        else:
            await SEX('▶️ *Неверная ссылка 5LIFE* ⛔️ *Отмена ввода*', context, FORMAT='B')
        return await REFER_FULL(update, context)
 
        
    if (step==25):       # stage 25       enter AI FREYA 
        print(" > Ручной ввод AI FREYA")
        return await FREYA_REQ(msg, context)
   
        
    if (step > 29):      # stage 9 LAST 9 echo then exit  ECHO MODE Репликатор
        await delete_user_message(update, context)
        print(" > Финальный Репликатор")
        mess = TextBlock('fin_bold')
        mess = mess.format(msg=ESU(msg))
        return await SEX(mess, context, FORMAT='B')
    elif (step > 0):      # exit stage 2 3 pass login
        await delete_user_message(update, context)
        print(" Было удалено как мусор")




async def BUTTON_RUN(choice, update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Получен callback c кнопки: {choice}")
    
    if choice == 'registration': # --NEW!!!          
        await START_JOIN2(update, context)
        
    elif choice.startswith('setrole_'): # --NEW!!! 
        role_index = int(choice.split("_")[1])        
        await SETUP_ROLE(role_index, update, context)
        
    elif choice == 'begin_game': # --NEW!!!          
        await Start_ROLES(update, context)  
        
    elif choice == 'life_book': # --NEW!!!          
        await START_BOOK(update, context)     
    
    elif choice == 'start_pro': # --NEW!!!          
        await START_PRO(update, context)
        
    elif choice == 'start_new': # --NEW!!!          
        await START_NEW(update, context)           
  
    elif choice == 'start_day': # --NEW!!!          
        await START_DAY(update, context)     

       
    elif choice == 'refer_menu': # -------------------------------REFERAL-PANEL
        Update_step(19, context)  # Silent Hill
        print("🤝 РЕФЕРАЛЬНАЯ ПРОГРАММА 🫱🏻")
        await REFER(update, context)

    elif choice.startswith('🤝'):  # --------REF-MENU_H
        await REFER_RUN(choice, update, context)             
    
    # elif choice == 'refer_partner': # -------------------------------REFERAL-PANEL
        # Update_step(19, context)  # Silent Hill
        # print("🤝 ПАРТНЕРСКАЯ КАБИНЕТ 🫱🏻")
        # await REFER_FULL(update, context)


             
    # elif choice == 'pay_refuse': # --NEW!!!          
        # await SEX('Никаких НАЗАД 😡\nсрочно плати', context, FORMAT = 'B') 
        # await START_PRO(update, context)
        
    elif choice == 'pay_back': # --NEW!!!          
        # await SEX('Никаких НАЗАД 😡\nсрочно плати', context, FORMAT = 'B') 
        await START_PRO(update, context)        
        
    # elif choice == 'pay_help': # --NEW!!!          
        # await SEX('Пишите 💻 [Менеджер](https://t.me/Bodyagolos)', context)  

    elif choice == 'pay_go': # --NEW!!!          
        await INPAY(context) 
        
    elif choice == 'pay_ok': # --NEW!!!          
        await INPAIMENT(context)     

    elif choice.startswith("pay_"): 
        tar_index = int(choice.split("_")[1])          
        await IN_TARIF(tar_index, context) 
        
   
    elif choice == 'more_info': # --NEW!!!          
        await MORE_INFO(context)     


    elif choice == 'freya_run': # --freya_run!!!          
        await FREYA_URUN(context)
        
    # elif choice == 'freya_final': # --FREYA_FINAL!!!          
        # await FREYA_FINAL(context)        
        

    elif choice == 'run_shop': # --GO_SHOP!!!          
        await GO_SHOP(update, context)          
   
    elif choice == 'roadmap': # --roadmap!!!          
        await Roadmap(update, context)
   
        
    elif choice.startswith("hometask_"):
        task_index = int(choice.split("_")[1])
        Set_Var ('cur_task', task_index, context)
        await Job_TASK(task_index, update, context)
    
    elif choice == 'back_menu': # -------------------------------RE-START-DAY
        Update_step(4, context)
        await START_AGAIN(None, update, context)
        
    elif choice == 'enter_name':# -------------------------------INPUT-USER-NICKNAME
        step = Get_Var('step', context)
        print(f"- Пришло сообщение с кнопки ИМЯ. Step={step}")
        if step>1:
            return
        # Update_step(1, context)
        textbut = Get_Var ('text_input_name', context)
        textbut += " 👇🏻"
        # Set_Var ('name_prompt_content', textbut, context)
        buttons = [[InlineKeyboardButton(textbut, callback_data='enter_name')]]
        keyb1 = Make_KEYB(buttons)

        await SEX(None, context, EDIT=Get_Var('mid_input_name', context), MENU=keyb1)

        return # await INPUT_RUN(None, update, context)
   
    elif choice == 'edit_name': # -------------------------------EDIT-NAME
        Update_step(5, context)
        await SEX("Введите исправленный ответ 🫱🏻\n_Не забудьте скопировать ответ перед правкой_ \n_иначе старый ответ будет перезаписан новым_",context, FORMAT='B')
    elif choice == 'homejob':   # -------------------------------HOMEJOB
        Update_step(4, context)
        await Start_HJ(update, context)

    elif choice == 'helpdesk':  # -------------------------------HELP
        Update_step(19, context)  # Silent Hill
        print("Выводим список команд бота")
        # text = "📨 У нашего бота есть *команды быстрого перехода* к различным *меню* или иным *функциям.* \n📣 *Вы можете свободно использовать все доступные Вам команды для Вашего комфорта*"
        # await SEFoB('helpdesk', text, context)
        # Set_Var ('mark_Helped', True, context)
        await Adelay(0.5)
        await Help_BLOCK(update, context)
    elif choice == 'fedesk':     # -------------------------------FEED
        Update_step(19, context)  # Silent Hill
        text = "☎️ Обратная связь 💁🏻 Отправить нам сообщение"
        print(text)
        # await SEM(text, context)     # await MAKE_DAYBACK(context)
        await Feed_MENU(update, context)
    elif choice.startswith('🎅🏻'):  # --------MODERATOR_H
        await MODER_RUN(choice, update, context)
    elif choice.startswith('🆔'):  # --------MOD-CON_H
        await MOD_RUN(choice, update, context)
    elif choice.startswith('☎️'): # --------FEED-MENU_H
        await FEED_SEND(update, context)
    elif choice.startswith('🌐'):    # --------TIMEZONE_H Clear_RUN
        await AskTZ_CALLBACK(choice, update, context)
    elif choice.startswith('❌'):    # --------Reset_RUN
        await Reset_RUN(choice, update, context)
    elif choice.startswith('⏰'):    # --------Crons_RUN
        await Crons_RUN(choice, update, context)       



async def BugSpy_Handler(message, context: ContextTypes.DEFAULT_TYPE):
    BUG_CHAT_id = PAY_CHAT_id
    user_nick = Get_Var('user_nick', context)
    user_id = Get_Uid(context)
    # SUP_CHAT_id = Get_Var('SUP_CHAT_id', context)
    head = f"{user_nick} 🆔:{user_id}"
    smi = "🏛" if PUB else "🧩"
    head = smi + ' > ' + head
    head = Form_Port(18, head)
    print(f"HEAD > {head}")
# Пересылаем сообщение LIFE_CHAT_id LIFE_CHAT_id SUP_CHAT_id
#  message.text or or message.video or message.audio or message.voice 
    step = Get_Var('step', context)
    if step==9:    
        if message.photo: 
            await context.bot.forward_message(chat_id=BUG_CHAT_id, 
            from_chat_id=message.chat.id, message_id=message.message_id)
            Update_step(19, context)  # Silent Hillp
            return await INPAID(context)
        
        elif message.document:
            DOC = message.document
            MIM = DOC.mime_type
            if MIM.startswith("image/") or MIM.startswith("application/pdf"):
                await context.bot.forward_message(chat_id=BUG_CHAT_id, 
                from_chat_id=message.chat.id, message_id=message.message_id)
                Update_step(19, context)  # Silent Hillp
                return await INPAID(context)
        # else:
            # return
                
    # else:        
    if message.text or message.voice or message.document or message.photo:
        await context.bot.forward_message(chat_id=BUG_CHAT_id, from_chat_id=message.chat.id, 
        message_id=message.message_id)
            
            # Update_step(19, context)  # Silent Hillp
            # await INPAID(context)
            
#               --------DEV-------------
def MOD_user_responses(day, user_id):
    # maxy = Getask_day(wday)
    # Срез day_responses до maxy   
    print (f"MOD_user_responses {day} {user_id} ")
    day_responses = Get_day_responses(day, user = user_id)
    # div_len = 42
    div = "="*42
    dv = "-"*73
    if day_responses is not None:
        dayz = CYFER(str(day))
        response_text = f"Ответы Игрока за {dayz} день\n{div}\n"
        for i, response in enumerate(day_responses, 1):  
            mark = '✅' if response else '☑️'
            if i==3:
                question = get_question(day)
                quest = f"{question}❔\n"
            else:
                quest = ""    
            t_name = TASKS[i-1]
            response = f"{dv}\n{response}" if response else ""
            response_text += f"Задание {i}: {mark}{t_name}\n{quest}{response}\n{div}\n"
        return response_text
    else:
        return f"Нет доступных ответов {day} дня!"

def get_u_works(user_id):
    """get_uwork value for any user"""
    return read4db('daywork', sender=user_id)

def get_u_day(user_id):
    """get_day value for any user"""
    return read4db('day', sender=user_id)



async def MOD_user_ANSW(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = Get_Var('mod_uid', context) # local2
    day = get_u_day(uid) # local2 
    # wday = get_u_works(uid)
    answers1 = MOD_user_responses(day, uid)
    await SEX(answers1, context)

async def MOD_user_JOB(update: Update, context: ContextTypes.DEFAULT_TYPE):
    Update_step(20, context)
    await SEX('🧩 Введи команду:', context)

async def MOD_MUD(mud:int, context: ContextTypes.DEFAULT_TYPE):
    Update_step(19, context)
    # save_uwork(mud)
    save_day(mud)
    await SEX(f'Обновлено ProgresDAY={mud}', context)


async def MOD_LUD(lud:int, context: ContextTypes.DEFAULT_TYPE):
    Update_step(19, context)
    await Inc_Lives(context, lives=lud)
    await SEX(f'Добавлены жизни: +{lud}', context)


async def MOD_Input_User(context: ContextTypes.DEFAULT_TYPE):
    text = "Введите порядковый № юзера в базе >"
    Update_step(12, context)
    return await SEX(text, context)

async def MOD_Input_PM(context: ContextTypes.DEFAULT_TYPE):
    text = "Введите в чате 1 сообщение для текущего Юзера:"
    Update_step(16, context)
    return await SEX(text, context)


async def MOD_CON(context: ContextTypes.DEFAULT_TYPE, update: Update = None):
    # if not await ALLOWED(context):      # ТЕСТИМ КМ на АДМИНЕ
    if not await ALLOW_DEV(context):
        return
    Update_step(12, context)
    print("🧩 КОНСОЛЬ МОДЕРАТОРА > Активирован Ввод Номера Юзера, step=12")
    Set_Var('mid_Mod_Job', None, context)
    user_unid = Get_VAR('mod_unid', 1, context)
    text = f"🧩 КОНСОЛЬ МОДЕРАТОРА 🧩 Выбран Юзер ▶ {user_unid}"
    print(text)
    selcap = f"{user_unid}"
    results = get_user_info(user_unid)
    if results:
        u_id, user_nick, user_name, user_status = results
        # stats = get_status_smile(user_status) # 🔢
        selcap +=f" 👤{user_nick} 🆔{u_id} 🕰{user_status}"
        Set_Var('mod_uid', u_id, context)
        Set_Var('mod_una', user_name, context)
        Set_Var('mod_uni', user_nick, context)
        Set_Var('mod_ust', user_status, context)
    # selcap = f"🔛{selcap}"
    button10 = InlineKeyboardButton(selcap, callback_data='🆔user_inf')
    # button21 = InlineKeyboardButton("📜 Данные", callback_data='🆔user_inf')    
    button21 = InlineKeyboardButton("📟 Терминал", callback_data='🆔user_job')
    button22 = InlineKeyboardButton("💬 Послание", callback_data='🆔pm2user')
    button31 = InlineKeyboardButton("👥 Каталог", callback_data='🆔list')
    button32 = InlineKeyboardButton("🔝 Закончить", callback_data='back_menu')
    buttons  = [[button10], [button21, button22], [button31, button32]]
    return await Make_MENB(text, buttons, context) #Make_KEYB(buttons)

async def MOD_UPAGE(context: ContextTypes.DEFAULT_TYPE, page: int = 1) -> None:
    limit = 16
    offset = (page - 1) * limit
    total_users = Get_VAR('users_count', 1, context)
    # if total_users<limit:
    limit = min(total_users, limit)
    users = print_users_limit(offset, limit)
    if not users:
        stata = "*Нет пользователей для показа* 🙅🏼"
        # await SEX(stata, context)
    else:
        stata = f"Подробный каталог *Юзеров👤{total_users}*📖Страница🧾{page}"
        # print ("ПКП > ")
        # print(users)
        for user in users:
            uid = user[0]
            uids = str(uid).zfill(2)
            tuid = user[1]
            name = ESU(user[2])
            nick = ESU(user[3])
            # stat = user[4]
            # stats = get_status_smile(stat) # 🔢
            stata += f"\n{uids} 👤 {name} 🆔 {tuid} 🎅🏻 {nick}"
# Добавим навигацию по страницам
    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton("⬅️Назад", callback_data=f'🆔spage_{page-1}'))
    if offset + limit < total_users:
        buttons.append(InlineKeyboardButton("Вперед➡️", callback_data=f'🆔spage_{page+1}'))
    buttons.append(InlineKeyboardButton("Выйти 👆🏻 Консоль", callback_data='🆔recon'))
    keyboard = InlineKeyboardMarkup([buttons])
    # await MOD_CON(context)
    await SEX(stata, context, MENU=keyboard, FORMAT='B')

async def MOD_USERS(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user_id = Update_UID(update, context)
    # await SEX("⌛️", context)
    count = get_users_count()
    Set_Var('users_count', count, context)
    stata = f"Количество пользователей в нашей базе: {count}"
    print(stata)
    # await delete_user_message(update, context)
    await SEX(stata, context)
    await MOD_UPAGE(context)

async def MOD_USEFORM(context: ContextTypes.DEFAULT_TYPE):
    user_unid = Get_VAR('mod_unid', 1, context)
    uids = str(user_unid).zfill(2)
    user_info = '' 
    print ( f"🧩 МОДЕРАТОР 🧩 > Досье на Игрока 🔢{uids}\n")
    full = get_user_full(user_unid)
    # //user[1]
    user_name = ESU(full[2])
    div = '▪️'*15
    st = full[6]
    stime = shot(st) if st else "Не запущена"
    refer = full[20] # f"🔢 индекс: {uids}\n"
    # text += str(get_user_info(user_unid))
    # user_nick = ESU(full[3])
    # uid = full[0]
    # status = int(full[6]) if full[6] else 0
    # stats = get_status_string(status)
    # statsm = get_status_smile(status)
    refer_str = f"🍕 Пригласивший в Игру: {refer}\n" if refer else ''
    # pays = full[11]
    # print ('PAYS=', pays)
    # preme = Get_User_Tarife(pays)
    user_info += (
    # f"{div}\n"
    f"🔢 Порядковый номер: {uids}\n"
    f"👤 Имя в Telegram: {user_name}\n"
    f"🕒 Старт Игры: 🦚 {stime}\n"
    f"🆔 Telegram ID: {full[1]}\n"
    f"🌐 Часовой пояс: {full[15]}\n"
    # f"📆 Текукущая неделя: {full[5]}\n"    
    # f"📈 Рабочие дни: {full[7]}\n"
    # f"💚 Рабочие доли: {full[11]}\n"
    # f"💰 Статус оплаты ПРЕМИУМ: {preme}\n"
    # f"🤝 Роль: {full[10]}\n"
    # f"🤝 Реферальный код: {full[11]}\n"
    f"{refer_str}"
    f"{div}"
    )

    return str(user_info)



async def Userfo(context: ContextTypes.DEFAULT_TYPE, user:int = None):
    if user: # Внешний ЗАПРОС
        user_id = user
        div = '▪️'*15
        geoday = 0
        # day = read4db("day", sender=user_id)
        # wday = get_u_works(user_id)
        user_unid = read4db('id', sender=user_id)
        user_DATA = get_user_full(user_unid)
        stime = user_DATA[6]
        day = user_DATA[4]
        week = user_DATA[5]
        # wday = user_DATA[7]
        pays = user_DATA[12]
        user_nick = user_DATA[3]
        ref_code = user_DATA[19]
        ref_count = user_DATA[21]
        Lives, Vitas, Antes, Doles = user_DATA[8], user_DATA[9], user_DATA[10], user_DATA[11]
        user_rate = get_prolevel(user_DATA[14])
        user_rang = Check_USER_Rang(context, user_id)
        user_status = RANGS[user_rang]
        uids = str(user_unid).zfill(2)
        stimes = Show_Game_Time(stime)
        # f"🆔 Telegram_ID: {user_DATA[1]}\n"
        status = 'Не получен'
        # stime = shot(st) if st else "Не запущена"
        user_path_, user_path = Create_user_folders(MODERATOR_DIR, user_id)
        # stimes = "Нет данных"
        # status = int(user_DATA[6]) if user_DATA[6] else 0
        # stats = (status)
    
        
    else:   # Внутренний ЗАПРОС
        user_id = Get_Uid(context)
        # day =  Get_Var('day', context)
        day = Get_User_Day(context)
        geoday = Get_Var('day_pass', context) + 1
        # wday = get_uwork()
        week = get_uweek()
        user_nick = Get_Var('user_nick', context)
        status = jet_status(context)
        # user_status = Get_VAR('user_status', "игрок", context)
        user_stime = Get_Var('user_stime', context)
        user_rate = get_rating()
        stimes = Show_Game_Time(user_stime)  
        ref_count = get_ref_count()
        ref_code = get_ref_code()
        pays = get_pays()
        # Set_Var('user_reflink', ref_link, context) 
        # stat_string, 
        # ext_string = Ext_TS(status) # Ext_SS
        Lives, Vitas, Antes, Doles = Get_Credos()
        user_path = Get_Var('user_path', context)

# готовим фотографию
    ava_name = user_nick + ".jpg" # НОВ ФОРМАТ
    file_path = os.path.join(user_path, ava_name)
    if not os.path.isfile(file_path):
        await SEX("Пожалуйста подождите ♻️ идет запрос данных:", context)
        await Scroll_chat_down(context.update, context)
        file_path = await GetavaUser(user_id, user_nick, user_path, context)
# Формируем БЛОК -  Userfo  новый !!!
    # ref_count = get_ref_count()
    # ref_code = get_ref_code()
    ref_link = Comb_Reflink(ref_code)
    Set_Var('user_reflink', ref_link, context)
    ref_ssyl = f'[ССЫЛКА]({ref_link})'
    div = " "
    user_role = get_role()
    # link = Get_VAR('user_reflink', "нет ссылки", context)
    # hyp_link = f"[🤝ССЫЛКА]({link})"
    
    preme = Get_User_Tarife(pays)
    
    
    t0 = '⚜️*СТРАНИЦА СТАТУСА*⚜️'
    t1 = f'👤 ИМЯ: {user_nick}'
    t2 = f'🎩 РОЛЬ: {user_role}'
    t21 = f'🏅 ПРОГ-СТАТУС: {user_rate}'
    t22 = f'🎩 ПРЕМ-СТАТУС: {preme}'    
    t4 = f'🕒 ВРЕМЯ в игре: {stimes}'
    t31 = f'❤️ Жизни: {Lives}'
    t32 = f'🪙 Витасы: {Vitas}'
    t33 = f'💰 Атлы: {Antes}'
    t34 = f'💚 Доли: {Doles}'    
    t5 = f'📆 ДЕНЬ марафона: {geoday}'
    t51 = f'📈 ПРОГРЕСС-ДЕНЬ: {day} из 27'
    t52 = f"📆 Неделя: {week}"    
    t6 = f'🔸 Статус д/з: {status}' # ext_string
    t7 = f'⭐️ Рефералы: {ref_count}'
    t8 = f'🤝️ Реф.код: {ref_code}'
    t9 = f'🍕 Реф.линк: {ref_ssyl}'    
    text = "\n".join([t0, div, t1, t2, t21, t22, div, t31, t32, t33, div, t4, t5, t51, t52, t6, t34, div, t7, t8, t9])

# Чекаем и отправляем фотографию
    if file_path:
        with open(file_path, 'rb') as photo:              # Отправляем фотографию
            # await SEFB (text, photo, context)
            await SEX(text, context, FORMAT='B', DOC=photo)
    else:                                                 # Отправляем текст
        await SEX(text, context, FORMAT='B')
    if not user:
        Set_Var ('mark_Informed', 1, context)





async def MOD_USEFULL(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = Get_Var('mod_uid', context)
    await Userfo(context, user_id)
    await Adelay(0.3)
    user_info = await MOD_USEFORM(context)
    await Adelay(0.2)
    # buttons = [[InlineKeyboardButton("Выйти 👆🏻 Консоль", callback_data='🆔recon')]]
    # buttons.append(InlineKeyboardButton("Подробно 👩🏻 Юзер-Инфо", callback_data='🆔user_in2fo')
    # await Make_MENB(user_info, buttons, context)
    # keyboard = Make_KEYB([buttons]) # await SEX (user_infos, context, MENU = keyboard)
    await SEX(user_info, context, FORMAT = 'B')
    await MOD_CON(context)

async def MOD_RUN(choice, update: Update, context: ContextTypes.DEFAULT_TYPE):
    if choice.startswith('🆔spage_'):
        page = int(choice.split('_')[-1])
        print(f"МОДЕРАТОР > Каталог\Страница: {page}")
        return await MOD_UPAGE(context, page)
    elif choice == '🆔recon':
        await MOD_CON(context)
    elif choice == '🆔list':
        print("МОДЕРАТОР > Каталог всех Игроков")
        await MOD_USERS(update, context)
    elif choice == '🆔user_inf':
        print("МОДЕРАТОР > Подробная 1 инфа на Игрока")
        await MOD_USEFULL(update, context)
    # elif choice == '🆔user_in2fo':
        # print("МОДЕРАТОР > Подробная 2 user_info на Игрока")
        # await MOD_USER2FO(context)
    elif choice == '🆔user_job':
        print("МОДЕРАТОР > debug")        
        await MOD_user_JOB(update, context)
    elif choice == '🆔sel_user':
        print("МОДЕРАТОР > Выбрать Игрока")
        await MOD_Input_User(context)
    elif choice == '🆔pm2user':
        print("МОДЕРАТОР > Сообщение Игроку")
        await MOD_Input_PM(context)
    elif choice == '🆔job_ok':
        print("МОДЕРАТОР > Принять Отметки-Задачи")
        await MOD_OK(context)
    elif choice == '🆔job_all':
        print("МОДЕРАТОР > Отметить все")
        await MOD_ALL(context)
    elif choice.startswith('🆔task'):
        ins = choice.replace('🆔task','')
        print("МОДЕРАТОР > Отметка Задания")
        await MOD_TASK(ins, context)





def Get_User_Tarife(pays:int=0):
    tarr = get_tariff_infoby_index(pays)
    if (pays>0):
        Tarife = f'{User_Tarifes[1]}-{tarr}'
    else:
        Tarife = User_Tarifes[0]
    return str(Tarife)        
        
        
def jet_status(context: ContextTypes.DEFAULT_TYPE):
    day = Get_User_Day(context)
    # wday = get_uwork()
    taskflags = Check_user_flags(day)
    uf_ALL_fin = Is_ALL_fin(day, taskflags)    
    status = '✅ заполнено' if uf_ALL_fin else '❌ не заполнено'
    return status     





        




async def Crons_Form(context: ContextTypes.DEFAULT_TYPE):
    BLOKTEXT  = "\nВыберите задачу и нажмите функциональную кнопку\n_Используйте формат ввода времени_ *H:M* _либо_ *H-M*"  
    buttons = []
    task_arr = Get_Var('crons_arr', context)
    task_list = Get_Var('crons_list', context)
    cur_task = Get_Var('crons_task', context)
    FLAG = False
    for i, task in enumerate(task_arr):
        taskname = task[0]
        tasktime = task[1]
        inx = i+1
        callback = f"⏰_{taskname}"
        flag = (cur_task==taskname)
        if flag:
            FLAG = True
        sign = '✅' if flag else ' '
        textbut = CYFER(str(inx))+sign+tasktime+' '+taskname[:12].upper()     
        buttons.append([InlineKeyboardButton(textbut, callback_data=callback)])
    TEXT = "⏰" + task_list + BLOKTEXT   
    caprun = "⏰Запустить"
    capren = "👉🏻Перенести"
    caprem = "❌Удалить"
    capadd = "🛎Добавить⏰"
    capext = "🔝Выход🔙"
    if FLAG:
        caprun+='☑️'
        capren+='☑️'
        caprem+='☑️'
    buttons.append([InlineKeyboardButton(caprun, callback_data='⏰_runcron')])
    buttons.append([InlineKeyboardButton(capren, callback_data='⏰_editcron')])
    buttons.append([InlineKeyboardButton(caprem, callback_data='⏰_delcron')])
    buttons.append([InlineKeyboardButton(capadd, callback_data='⏰_addcron')])
    buttons.append([InlineKeyboardButton(capext, callback_data='begin_game')])
    return TEXT, buttons
    
async def Crons_LIST(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ALLOWED(context):        
        return
    print("> Админ - Вывести список задач кронтаба:")
    task_arr, task_list = cron_tasks(update, context)
    Set_Var('crons_arr', task_arr, context)
    Set_Var('crons_list', task_list, context)
    Text, Buttons = await Crons_Form(context)    
    message = await Make_MENB(Text, Buttons, context)  
    Set_Var('mid_Crons', message.message_id, context) 



async def Crons_RUN(choice, update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = Get_Uid(context)
    cur_task = Get_Var('crons_task', context)
    if choice == '⏰_runcron': # Запущивание задачи
        if cur_task:
            await Crons_TEST(cur_task, context)
            return await Crons_LIST(update, context)
        else:
            return await SEX("Сначала выберите задачу", context)
    elif choice == '⏰_editcron': # Запрос нового времени
        if cur_task:
            Update_step(14, context)    
            return await SEX("Введите новое время", context)
        else:
            return await SEX("Сначала выберите задачу для правки", context)
    elif choice == '⏰_addcron': # Дабавливание
        Update_step(15, context)    
        return await SEX("Введите новую задачу в формате:\nИМЯ_ЗАДАЧИ (запятая) ВРЕМЯ_ЗАПУСКА ☑️", context)
    elif choice == '⏰_delcron': # Удаливание
        if cur_task: 
            if cur_task=='alarm_report':
               return await SEX('⛔️ Вы не можете удалить ❌ эту задачу ⛔️\nОна служебная и должна находиться в суточном Кронтабе 🧐', context) 
            text = remove_task(cur_task)
            Set_Var('crons_task', None, context)
            print(text)
            await SEX(text, context)
            return await Crons_LIST(update, context)
        else:
            return await SEX("Сначала выберите задачу для удаления", context)
    else:          # Выбирывание задачи
        Task = choice[2:] # index=choice[2:] # inx = int(index)
        Set_Var('crons_task', Task, context)
        print ("Записано crons_task: ", Task)
        Text, Buttons = await Crons_Form(context)
        Keybs = Make_KEYB(Buttons)
        mid_Crons = Get_Var('mid_Crons', context)
        if mid_Crons:
            Old_Text = Get_Var('crons_oldmes', context)     
            if Old_Text and Text!=Old_Text:  # , FORMAT='B'
                await SEX(Text, context, EDIT=mid_Crons, MENU = Keybs) 
                Set_VAR('crons_oldmes', Text, context)
            else:
                await SEX(None, context, EDIT=mid_Crons, MENU = Keybs)         
        else:
            message = await Make_MENU(Text, Buttons, context)  
            Set_Var('mid_Crons', message.message_id, context) 


async def Crons_Add_New(msg, context: ContextTypes.DEFAULT_TYPE):
# Функция для запроса новой задачи у пользователя
    user_id = Get_Uid(context)
    cur_task = Get_Var('crons_task', context)
    Update_step(19, context)
    if msg:
        if not ',' in msg:
            pass
        t_name, t_time = map(str, msg.split(','))               
        to_time = S2TIME(t_time)     
        text = add_task(t_name, to_time, context)
        await SEX(text, context)  
        return await Crons_LIST(context.update, context)
    await SEX("Отмена операции", context)     
   
async def Crons_Edit(msg, context: ContextTypes.DEFAULT_TYPE):
# Функция для запроса нового времени у пользователя
    user_id = Get_Uid(context)
    cur_task = Get_Var('crons_task', context)
    Update_step(19, context)
    if msg:
        to_time = S2TIME(msg)          
        text = edit_task(cur_task, to_time, context)
        await SEX(text, context)  
        return await Crons_LIST(context.update, context)
    await SEX("Отмена операции", context) 
    
async def FEED_GO(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    # await SEX("📩 Составить отчет об ошибке", context)
    await Write_BUG(update, context) 
  
async def FEED_SEND(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    # await SEX("📩 Составить отчет об ошибке", context)
    await Send_BUG(update, context) 

async def END_book(context: ContextTypes.DEFAULT_TYPE):
    await SEX_PRO('LB_PAUSE', context)

async def Icons_BLOCK(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await SEX_PRO('ICONS', context)

async def Roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await SEX_PRO('ROAD-MAP', context)    
    text, keyboard, picture_path = Make_Block('ROADMAP')
    text = text.format(VER)
    Block_Pk = text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context)


  

async def Help_BLOCK(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text, keyboard, picture_path = Make_Block('HELP_USER')
    if ADM or REV:
        message2, keyboard, picture_path = Make_Block('HELP_ADMIN')
        message_text = message_text + "\n" + message2     
    message_text = message_text.format(VER = VER)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context)      

def get_last_log(log_file:str, log_limit:int):
    with open(log_file, 'r', encoding='utf-8') as file:
        logs = file.readlines()
    if logs:
        cut_lines = logs[-log_limit:]
        return "".join(cut_lines)
    else:
        return "Логи отсутствуют."


async def Set_DAY(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await ALLOWED(context):
        return
    print(" > Админ - Set_DAY")
    if context.args:  # Проверка наличия аргумента
        try:
            cargo = context.args[0]
            if isinstance(cargo, str) and cargo.lower() == 'auto':
                new_day = AUTODAY(context)
                if new_day:
                    await SEX(f'Автонастройка дня, новый день: {new_day}', context)
                    Update_step(19, context)  # Silent Hill
                    await Start_ROLES(update, context)
                return
            newday = int(cargo)
            if 1 <= newday <= MAX_DAYS:
                Update_step(19, context)  # Silent Hill
                await UMR(f"Вы выбрали день: {newday}", update)
                Set_Var('day', newday - 1, context)
                await Inc_Day(context)  # теперь НЕ вызывает рестарт
                await Start_ROLES(update, context)
            else:
                Update_step(6, context)
                await UMR(f"Пожалуйста, введите число от 1 до {MAX_DAYS}!", update)
        except ValueError:
            Update_step(6, context)
            await UMR("Пожалуйста, введите корректное число!", update)
    else:
        Update_step(6, context)
        await UMR(f"Пожалуйста, укажите номер дня: [1-{MAX_DAYS}]", update)


async def MIG_RUN(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ALLOW_DEV(context):
        return
    print(" > Супер-Админ - MIG_RUN")
    if context.args:  # Проверка наличия аргумента
        try:
            migra = str(context.args[0])
            print(" > поступил аргумент - MIGRA:", migra)
            clear_migra = migra.replace('@','')
            clear_migra = clear_migra.replace('#','')
            # special = False
            # if '+' in migra:
                # special = True
                # migra = migra.replace('+','')
            print(" > обработан аргумент - MIGRA:", clear_migra)    
            if os.path.exists(clear_migra):
                res = migrate_data(migra)  # 'book.sql'
                await SEX(res, context)
                # Send_STICKER(52, context)
                Sdelay(2)
                Update_step(19, context)  # Silent Hill
                await START_LIFE(update, context)
            else:
                Update_step(19, context)
                await UMR("Неверный аргумент. Миграция отменена", update)
        except ValueError:
            Update_step(19, context)
            await UMR("Неверный аргумент. Миграция отменена", update)
    else:
        Update_step(17, context)
        await UMR("Введите основной аргумент для Миграции", update)
        


async def MAKE_DAYBUCK(msg:str, context: ContextTypes.DEFAULT_TYPE):
    but1 = InlineKeyboardButton("Страница Статуса"  , callback_data='back_menu')
    but2 = InlineKeyboardButton("Панель Помощи", callback_data='helpdesk')
    buttons = [[but1, but2]]
    return await Make_MENB(msg, buttons, context)



# Фрея - запуск с команды  FREYA_AICON
async def FREYA_RUN(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ALLOWED(context):
        return
    print(" > Админ - FREYA_RUN")     
    Update_step(25, context)
    await SEX_PRO('FREYA_AICON', context)


# Фрея - запуск с кнопки  FREYA_AIRUN
async def FREYA_URUN(context: ContextTypes.DEFAULT_TYPE):
    print(" > Юзер - FREYA_RUN")
    Update_step(25, context)
    await SEX_PRO('FREYA_AIRUN', context)     


# формирование текст запроса в Фрею   
async def FREYA_REQ(text, context: ContextTypes.DEFAULT_TYPE):
    name = Get_Var ('user_nick', context)
    # uname = Get_Var ('user_name', context)    
    u1name = f'name={name}'
    # u2name = f'telegram name={uname}'
    # urname = f'{u1name} {u2name}'
    uraname = f'[{u1name}]' if u1name else ''
    # text = uraname+text;
    print(" > FREYA_REQ - text=", text)
    print(" > FREYA_REQ - urname=", uraname)
    return await INHA_TEX(text, uraname, context)


# ИИ задача на 14 дня - 1 проверка выполнения домашки + ремандер
async def FREYA_DAYJOB(context: ContextTypes.DEFAULT_TYPE):
    day = Get_User_Day(context) # получили ДЕНЬ
    # wday = get_uwork()
    taskflags = Check_user_flags(day)   # получили taskflags через ДЕНЬ
    uf_ALL_fin = Is_ALL_fin(day, taskflags)   # получили uf_ALL_fin через ДЕНЬ + taskflags
    # message = ">🧑🏻‍🎓> Процедура проверки выполнения задания: "    
    # if uf_ALL_fin:   return    # если 3 домашки готово - выход нет алярма    !!!!!!!!!!!!!!!!!!!!!
    req_alarm = FREY_A_LARM(context) 
    saveit('FREY_A_LARM', req_alarm)
    print(" > FREYA_DAYJOB - req_alarm=", req_alarm)
    return await INHA_TEX(req_alarm, '', context)

# ИИ задача на 14 дня - 2 БЛОК-ЗАПРОС
def FREY_A_LARM(context: ContextTypes.DEFAULT_TYPE):  # анализ дня - спец вопрос
    name = Get_Var ('user_nick', context)  
    # await SEX(f'{message} OK ✅', context)        
    day = Get_User_Day(context) # получили ДЕНЬ
    # wday = get_uwork()
    taskflags = Check_user_flags(day)   # получили taskflags через ДЕНЬ
    uf_COUNT = Is_AFK(day, taskflags)    
    mex = '\nИгрок даже не приступал!' if uf_COUNT<1 else ''      
    return (
    'Результат проверки заполнения Дневника или задания дня на сегодня:\n'
    f'Имя Игрока: {name} \n'
    f'Заполнено ответов дня: {uf_COUNT} из 3.'
    f'{mex}'
    '\n Задача в 14:00. Придумай хороший ответ чтобы напомнить мне о необходимости продолжить выполнение задания дня, то есть заполнить оставшиеся ответы дневника, не забудь написать про команду /daily которая позволит игроку сразу перейти в дневник. Но если игрок заполнил все 3 ответа из 3 просто похвали его и напомни ему, что его ждет вечерний разбор ответов в 18-00.'
    )    
    
    
async def FREYA_PUSH(msg:str, update: Update, context: ContextTypes.DEFAULT_TYPE):  
    if msg.startswith('0'):
        Update_step(19, context) # last silence Step
        return await UMR(f"Отмена команды, bash stopped", update)         

    if msg.startswith('a'):
        return await MOD_user_ANSW(update, context)

    if msg.startswith('f'):
        msg = msg[1:]
        # if msg.isdigit():
            # code = int(msg)
        # if msg == '0':
            # await UMR(f"PUSH > Вызов FREYA_DAYJOB", update)
            # Update_step(19, context) # last silence Step                    
            # return await FREYA_DAYJOB(context)  
        if msg == '1':
            await UMR(f"PUSH > Вызов FREYA_DAYJOB", update)
            # Update_step(19, context) # last silence Step                    
            return await FREYA_DAYJOB(context)          
        if msg == '2':
            await UMR(f"PUSH > Вызов FREYA_EVENING", update)
            # Update_step(19, context) # last silence Step                    
            return await FREYA_EVENING(context)  
        if msg == '3':
            await UMR(f"PUSH > Вызов TEST_EVENING", update)
            # Update_step(19, context) # last silence Step                    
            return await TEST_EVENING(context) 

    if msg.startswith('l'):
        msg = msg[1:]
        if msg.isdigit():
            cofe = int(msg)
            if 1 <= cofe <= 99:
                return await MOD_LUD(cofe, context)
        await UMR(f"Ошибка: Жду корректное значение аргумента от 1 до {99}", update)
        return



    if msg.startswith('u'):
        msg = msg[1:]
        if msg.isdigit():
            cofe = int(msg)
            if 1 <= cofe <= MAX_DAYS:
                return await MOD_MUD(cofe, context)
        await UMR(f"Ошибка: Жду корректное значение аргумента от 1 до {MAX_DAYS}", update)
        return

    Update_step(19, context) # last silence Step
    return await UMR(f"Ошибка команды, bash stopped", update)    

# ИИ  задача на 18 дня -ТЕСТ- 1 Анализ главного вопроса дня отключено
async def FREYA_EVENING(context: ContextTypes.DEFAULT_TYPE):  # Фрея на 18 - Кормим
    FULL = not True
    print ('FREYA_EVENING_FEED_RUN 18 > FULL=', FULL)
    day = Get_User_Day(context) # получили ДЕНЬ
    # wday = get_uwork() # получили pДЕНЬ
    # name = Get_Var ('user_nick', context)  
    # uf_COUNT = Is_AFK(day, taskflags)    
    taskflags = Check_user_flags(day)   # получили taskflags через ДЕНЬ
    uf_ANY_fin = Is_ANY_fin(day, taskflags)   # получили uf_ALL_fin через ДЕНЬ + taskflags
    if not uf_ANY_fin:   return    # если ни одного ответа - выход   
    
    user_id = Get_Uid(context)
    # answers = MOD_user_responses(day, user_id, 3) 
    answers = Get_day_responses(day, user = user_id)
    print ('FREYA_FEED answers > ', answers)  
    answer = answers[2] if answers[2] else None
    if not answer:   return    # если нет спец. ответа - выход   
    
    answer = answer or "Нет"
    
    if FULL:
        if answers[0]:
            addan = f'\nТакже ответ на вопрос «{TASKS[0]}»\n{answers[0]}'
            answer += addan
        if answers[1]:
            addan = f'\nТакже ответ на вопрос «{TASKS[1]}»\n{answers[1]}'
            answer += addan
    
    print ('FREYA_FEED answer > ', answer)    
    # question = questions if questions else "Нет" 
    question = get_question(day) or "Нет"
    print ('FREYA_FEED question > ', question) 
    
    frequest = FREY_A_DAY(question, answer, context)
    saveit('FREY_A_DAY.txt', frequest)
    
    print("FREYA_FEED from FREY_A_DAY frequest > ", frequest)
    return await INHA_TEX(frequest, '', context)    



def saveit(fname, text):
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(text)

# ИИ  задача на 18 дня -ТЕСТ- 2 - БЛОК-ЗАПРОС
def FREY_A_DAY(question, answer, context: ContextTypes.DEFAULT_TYPE):  # анализ дня - спец вопрос
    name = Get_Var ('user_nick', context)  

    task = ('Форма анализа (Задача вечерняя на 18:00 для каждого дня)\n'
    'После ответа человека на вопрос дня ты формируешь короткий текст в формате:\n'
    '🔹 Наблюдение за нарративом.\n'
    'Пример: «Ты описываешь себя через действия и достижения — возможно, твоя ценность для себя связана с пользой»\n'
    '🔹 Возможный внутренний конфликт.\n'
    'Пример: «Ты хочешь быть настоящим, но пишешь о том, как важно соответствовать»\n'
    '🔹 Подсвечивание силы\n'
    'Пример: «В том, что ты позволяешь себе такие признания — уже твоя зрелость»' )
    
    return (
    'Нужно провести анализ главного (№3) ответа дня игрока на сегодня:\n'
    f'Имя Игрока: {name} \n'
    f'ВОПРОС ДНЯ: {question}\n'    
    f'ОТВЕТ ДНЯ: {answer}\n'
    f'АЛГОРИТМ: {task}\n'
    'Выдай ответ в стиле Вечерний Анализ\n'
    'Важное замечание: на нужно анализировать каждый ответ отдельно если много ответов - дай суммарный анализ'
    )
 
# задача сделать блок за 7 дней
async def FREYA_WEEK(context: ContextTypes.DEFAULT_TYPE):  # Фрея TEST1
    print ('FREYA_WEEK > ')
    frequest = FREY_A_WEEK(context) 
    saveit('FREYA_WEEK.txt', frequest)    
    print("FREYA_WEEK frequest > ", frequest)
    return await INHA_TEX(frequest, '', context) 

# задача БЛОК-ЗАПРОС  анализ  7 дней
def FREY_A_WEEK(context: ContextTypes.DEFAULT_TYPE): 
    name = Get_Var ('user_nick', context)  
    # quest1 = TASKS[0]
    # quest2 = TASKS[1]     
    # answers = '\n'.join([ans3, ans1, ans2])
    answers = Get_all_responses()
    print (f'FREY_A_WEEK Недельный отсчет:\n{answers}')
    test_task = ('Структура промежуточного анализа:\n'
    '🔹 Главный нарратив, который звучит в ответах «На протяжении этого блока прослеживается история о…»\n'
    '🔹 Ключевой фильтр восприятия (вопрос, страх, ожидание) «Похоже, ты часто смотришь на себя/мир через идею о…»\n'
    '🔹 Ресурс или сила, которая уже в тебе есть «В каждом ответе звучит сила, с которой ты…» \n'
    )    
    return (
    'Сегодня 7-й день, наш Игрок закончил неделю марафона. Нужно провести НЕДЕЛЬНЫЙ РАЗБОР всего Дневника игрока и выдать целостный мини-анализ :\n'
    f'Имя Игрока: {name} \n'
    f'ВСЕ ОТВЕТЫ ЗА НЕДЕЛЮ:\n{answers}\n'
    f'АЛГОРИТМ: {test_task}'   
    )  



async def FREYA_TEST1(context: ContextTypes.DEFAULT_TYPE):  # Фрея TEST1
    print ('FREYA_TEST1 > ')
    # day = Get_User_Day(context) # получили ДЕНЬ  
    frequest = FREY_A_TEF1(context) 
    print("FREYA_TEST1 frequest > ", frequest)
    return await INHA_TEX(frequest, '', context)    
    
    
# задача на -ТЕСТ- 2 
async def FREYA_TEST2(context: ContextTypes.DEFAULT_TYPE):  # Фрея TEST2
    print ('FREYA_TEST2 > ')
    # day = Get_User_Day(context) # получили ДЕНЬ  
    frequest = FREY_A_TEF2(context) 
    print("FREYA_TEST2 frequest > ", frequest)
    return await INHA_TEX(frequest, '', context)    
    
# задача на -ТЕСТ- - БЛОК-ЗАПРОС  анализ финала 1в радость - Шаблон ответов
def FREY_A_TEF1(context: ContextTypes.DEFAULT_TYPE):  # анализ финала 1в радость
    name = 'Test Person' 
    quest1 = TASKS[0]
    # quest2 = TASKS[1] 
    ans1 = 'https://telegra.ph/Testovyj-SHablon-05-24' 
    # ans2 = 'https://telegra.ph/Testovyj-SHablon-2-05-24'    
    test_task = ('ГЛУБОКИЙ РАЗБОР, ИСХОДЯ ИЗ ОТВЕТОВ:'
    '🔹 Скрытые нарративы — что на самом деле управляет твоими решениями'
    '🔹 Непризнаваемый страх — то, чего ты избегаешь, но оно управляет жизнью'
    '🔹 Повторяющиеся петли — где ты снова и снова застреваешь'
    '🔹 Корневые триггеры — откуда всё началось'
    '🔹 Твой архетип — кем ты являешься по своей глубинной природе'
    '🔹 Парето-анализ (80/20) — что даёт тебе максимум, а что истощает'
    '🔹 Суть твоего “Я” — формула, в которой ты узнаешь себя, без искажений.')    
    return (
    'Нужно провести ГЛУБОКИЙ РАЗБОР 1 ответа Дневника игрока на финале марафона (28 дней):\n'
    f'Имя Игрока: {name} \n'
    f'Вопрос: {quest1}\n'
    f'ОТВЕТЫ:\n{ans1}\n'
    f'АЛГОРИТМ: {test_task}\n'
    'Выдай ответ в стиле "Финальный отчет"'    
    )   
    
    
# задача на -ТЕСТ- - БЛОК-ЗАПРОС  анализ финала полный фейк тест - Шаблон ответов
def FREY_A_TEF2(context: ContextTypes.DEFAULT_TYPE):  # анализ финала полный фейк тест
    name = 'Test Person' 
    quest1 = TASKS[0]
    # quest2 = TASKS[1] 
    ans1 = 'https://telegra.ph/Testovyj-SHablon-05-24'
    ans2 = 'https://telegra.ph/Testovyj-SHablon-2-05-24'
    ans3 = 'https://telegra.ph/Testovyj-shablon-otvetov-06-03'
    answers = '\n'.join([ans3, ans1, ans2])
    test_task = ('ГЛУБОКИЙ РАЗБОР, ИСХОДЯ ИЗ ОТВЕТОВ:'
    '🔹 Скрытые нарративы — что на самом деле управляет твоими решениями'
    '🔹 Непризнаваемый страх — то, чего ты избегаешь, но оно управляет жизнью'
    '🔹 Повторяющиеся петли — где ты снова и снова застреваешь'
    '🔹 Корневые триггеры — откуда всё началось'
    '🔹 Твой архетип — кем ты являешься по своей глубинной природе'
    '🔹 Парето-анализ (80/20) — что даёт тебе максимум, а что истощает'
    '🔹 Суть твоего “Я” — формула, в которой ты узнаешь себя, без искажений.'
    'Выдай ответ в стиле "Финальный отчет". Попробуй зафиксировать состояние Игрока на начало и конец марафона и выдать итоговый результат как улучшилось его состояние'
    )    
    
    return (
    'Сегодня 28-й день, наш Игрок закончил марафон. Нужно провести ГЛУБОКИЙ финальный РАЗБОР всего Дневника игрока и выдать полный финальный анализ:\n'
    f'Имя Игрока: {name} \n'
    f'ВСЕ ОТВЕТЫ ЗА МАРАФОН:\n{answers}\n'
    f'АЛГОРИТМ: {test_task}\n'   
    )     
    
# задача на -ТЕСТ- - БЛОК-ЗАПРОС  анализ финала все ответы Игрока из базы
def FREY_A_FIN(context: ContextTypes.DEFAULT_TYPE):  # анализ финала марафона
    user_id = Get_Uid(context)
    day = Get_User_Day(context) # получили ДЕНЬ
    # wday = get_uwork()
    name = Get_Var ('user_nick', context)  
    ANSWERS =  (day, user_id, 3)     
    task = ('ГЛУБОКИЙ РАЗБОР, ИСХОДЯ ИЗ ОТВЕТОВ:'
    '🔹 Скрытые нарративы — что на самом деле управляет твоими решениями'
    '🔹 Непризнаваемый страх — то, чего ты избегаешь, но оно управляет жизнью'
    '🔹 Повторяющиеся петли — где ты снова и снова застреваешь'
    '🔹 Корневые триггеры — откуда всё началось'
    '🔹 Твой архетип — кем ты являешься по своей глубинной природе'
    '🔹 Парето-анализ (80/20) — что даёт тебе максимум, а что истощает'
    '🔹 Суть твоего “Я” — формула, в которой ты узнаешь себя, без искажений.')
    return (
    'Нужно провести ГЛУБОКИЙ РАЗБОР ответов Дневника игрока на финал:\n'
    f'Имя Игрока: {name} \n'
    f'Заполнено ответов дня: {uf_COUNT} из 3\n'
    f'ОТВЕТЫ:\n{ANSWERS}\n'
    f'АЛГОРИТМ: {task}\n'
    'Выдай ответ в стиле "Вечерний Анализ"'    
    )   
    
    
# вопрос "Благодарность дня?" https://telegra.ph/Testovyj-SHablon-2-05-24
# вопрос "Радость дня?" https://telegra.ph/Testovyj-SHablon-05-24
# вопрос "особый Вопрос Дня" https://telegra.ph/Testovyj-shablon-otvetov-06-03    
    
    
     # user_id = Get_Uid(context)
    # day = Get_User_Day(context) # получили ДЕНЬ
    # name = Get_Var ('user_nick', context)      
    # taskflags = Check_user_flags(day)   # получили taskflags через ДЕНЬ
    # uf_COUNT = Is_AFK(day, taskflags)    
    # uf_ANY_fin = Is_ANY_fin(day, taskflags)   # получили uf_ALL_fin через ДЕНЬ + taskflags    
    # ANSWERS = MOD_user_responses(day, user_id, 3)  
    # user_id = Get_Uid(context)
    # day = Get_User_Day(context) # получили ДЕНЬ
    # taskflags = Check_user_flags(day)   # получили taskflags через ДЕНЬ
    # uf_COUNT = Is_AFK(day, taskflags)    
    # uf_ANY_fin = Is_ANY_fin(day, taskflags)   # получили uf_ALL_fin через ДЕНЬ + taskflags          
    # taskflags = Check_user_flags(day)   # получили taskflags через ДЕНЬ
    # uf_COUNT = Is_AFK(day, taskflags)    
    # uf_ANY_fin = Is_ANY_fin(day, taskflags)   # получили uf_ALL_fin через ДЕНЬ + taskflags      
    # question = get_question(day)
    # print ('FREY_A_DAY question > ', question)
    # answers = MOD_user_responses(day, user_id, 3) 
    # answer = answers[2] if answers[2] else "Нет" 
    # print ('FREY_A_DAY answer=answers[2] > ', answer)    
    