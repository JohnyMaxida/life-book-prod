"""
Новый корневой логический движок (orchestrator) для Life-Book бота.
Использует блоковую систему UI из lifeBlock.py через ui_blocks.py
Полностью портирован с logical_old.py на aiogram 3.x
"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandObject

from db_manager import DatabaseManager
from ui_blocks import (
    SEX, SEX_PRO, SEX_PROD,
    get_block as Make_Block,
    format_block_text,
    create_menu_from_block,
    Make_KEYB
)
from const import MAX_DAYS, MAX_STIX, ITEMS_PER_PAGE, TASKS, ROLES, User_Tarifes
from utils import (
    Get_Var, Set_Var, Update_step, Sdelay, Adelay,
    Check_User, Get_User_Day, Update_User_ZONE, save_timezone, save_role,
    get_role, get_credos, save_credos, get_pays, get_ref_count, get_ref_code,
    Check_user_flags, Is_ALL_fin, Is_ANY_fin, jet_status, get_rating,
    Comb_Reflink, pluralize_ru, get_uweek, save_uweek, user_progress,
    Inc_Lives, Inc_Vitas, save_day, get_question,
    Get_User_Tarife, Get_DOLE_FP, Set_DOLE_FP, Get_SHOW_FP, Set_SHOW_FP,
    Get_DONNA_FP, Set_DONNA_FP, Get_DONNA_URL, Get_UNI_URL, Get_AXI5M_URL,
    Prep_MOC4, Prep_MOC5, Get_VAR
)
from config import config
from logger import logger

# Import cron functions
try:
    from ambacron import CRON_AMBA1, CRON_AMBA2
except ImportError:
    logger.warning("Could not import CRON functions from ambacron")
    def CRON_AMBA1(context): return False
    def CRON_AMBA2(context): return False

# Import freya AI
try:
    from free11ray import AQnit, INHA_TEX
    from fre0gen import TuneGenPath
except ImportError:
    logger.warning("Could not import AI functions")
    AQnit = None
    INHA_TEX = None
    TuneGenPath = None

# Constants
N_TAX = len(TASKS)

# Chat IDs from config
LIFE_CHAT_ID = config.chats.life_chat_id
PAY_CHAT_id = config.chats.pay_chat_id
DEV_CHAT_id = config.chats.dev_chat_id

# Import other modules
try:
    from passive import SEMOD, END_book
except ImportError:
    logger.warning("Could not import passive module functions")
    async def SEMOD(text, keyboard, context): pass
    async def END_book(context): pass

try:
    from temporal import Ask_ZONE, Inc_Day, get_target_date
except ImportError:
    logger.warning("Could not import temporal module functions")
    async def Ask_ZONE(context): pass
    async def Inc_Day(context): pass
    def get_target_date(y, m, d): return None

try:
    from answers import Init_Answers
except ImportError:
    Init_Answers = None

try:
    from free11ray import FREYA_WEEK
except ImportError:
    async def FREYA_WEEK(context): pass

# Import InlineKeyboardButton for button creation
from aiogram.types import InlineKeyboardButton


# ===== MAIN FLOW FUNCTIONS =====

async def GLUBDATE(message: Message, context: FSMContext, db: DatabaseManager):
    """Global update function - initializes context variables."""
    user_id = message.from_user.id
    await context.update_data(user_id=user_id)

    # Set user path if TuneGenPath is available
    if TuneGenPath:
        TuneGenPath(user_id)

    # Get or create user in database
    user = await db.get_or_create_user(
        user_id=user_id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    return user


async def START_AGAIN(warn: str, message: Message, context: FSMContext, db: DatabaseManager):
    """Restart the bot flow - called after various operations."""
    await GLUBDATE(message, context, db)

    # Clear some context variables
    await context.update_data(mid_Show_Time=None, mid_Ask_Zone=None)
    Update_step(19, context)

    if warn and warn != '':
        await SEX(warn, context, FORMAT='B')
        Sdelay(1)

    # Check if user is new
    logger.info(">> Инициация бота пользователем > запрос данных...")
    uf_IsNew = not Check_User(context)
    await context.update_data(uf_IsNew=uf_IsNew)

    if uf_IsNew:  # new user
        await START_JOIN(message, context, db)
    else:  # existing user
        await START_LIFE(message, context, db)


async def START_JOIN(message: Message, context: FSMContext, db: DatabaseManager):
    """Start registration flow for new users - JOIN1."""
    Update_step(18, context)
    logger.info("Первый вход Юзера, приветствие, регистрация...")
    await SEX_PRO('JOIN1', context, message)


async def START_JOIN2(message: Message, context: FSMContext, db: DatabaseManager):
    """JOIN2 - Ask for user nickname."""
    logger.info("РЕГ > Ожидается Ввод юзером псевдонима...")
    Update_step(1, context)
    await SEX_PRO('JOIN2', context, message)


async def START_JOIN2_GOT(msg: str, message: Message, context: FSMContext, db: DatabaseManager):
    """Process nickname input from user."""
    logger.info("Запущен процесс регистрации")
    await context.update_data(user_nick=msg)
    Update_step(2, context)
    await START_JOIN3(message, context, db)


async def START_JOIN3(message: Message, context: FSMContext, db: DatabaseManager):
    """JOIN3 - Setup role (simplified to single role)."""
    logger.info("Теперь у всех 1 роль на входе")
    await SETUP_ROLE(1, message, context, db)


async def SETUP_ROLE(role_index: int, message: Message, context: FSMContext, db: DatabaseManager):
    """Save selected role and proceed to JOIN4."""
    logger.info("Сохраняем РОЛЬ в контекст...")
    role = ROLES[role_index] if role_index < len(ROLES) else ROLES[0]
    await context.update_data(user_role=role)
    text = f'▶️ Выбрана роль: {role}'
    await SEX(text, context, message, FORMAT='B')
    await START_JOIN4(message, context, db)


async def START_JOIN4(message: Message, context: FSMContext, db: DatabaseManager):
    """JOIN4 - Setup timezone."""
    logger.info("Ожидается выбор Час. Пояс/Зона...")

    # Check timezone in context
    state_data = await context.get_data()
    offset = state_data.get('user_tz')
    logger.info(f">After_Init> Ищем timezone в контексте: {offset}")

    if offset is None:
        logger.info(">After_Init> Часовой ПОЯС не задан > Пока ставим UTC=0")
        offset = 0

    Update_User_ZONE(offset, context)
    logger.info(f">After_Init> Обновляю ТЗ на основе offset={offset}")

    await Ask_TZ(message, context, db)


async def POST_PREP(message: Message, context: FSMContext, db: DatabaseManager):
    """Post-preparation - finalize registration or return to START_LIFE."""
    state_data = await context.get_data()
    uf_IsNew = state_data.get('uf_IsNew')
    offset = state_data.get('user_tz')

    if not uf_IsNew:
        if offset:
            save_timezone(offset)
        return await START_LIFE(message, context, db)

    logger.info("Регистрируем Юзера")
    user_id = await Reg_User(message, context, db)
    await context.update_data(uf_IsNew=None)

    logger.info(f'Тестируем вторичный user_id={user_id}')
    if not user_id or (user_id < 1):
        logger.error('Ошибка возврата user_id')
    else:
        logger.info('Обновляем user_id !!!')
        await context.update_data(user_id=user_id)

    # Initialize answers if available
    if Init_Answers:
        Init_Answers()

    save_timezone(offset)
    role = state_data.get('user_role')
    save_role(role)

    INCRES = CRON_AMBA1(context)
    logger.info(f"СТАРТУЕМ КРОНы > {INCRES}")

    await After_Init(message, context, db)
    await START_LIFE(message, context, db)


async def Reg_User(message: Message, context: FSMContext, db: DatabaseManager) -> int:
    """Register new user in database."""
    state_data = await context.get_data()
    user = await db.get_or_create_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        nickname=state_data.get('user_nick'),
        role=state_data.get('user_role'),
        timezone=state_data.get('user_tz', 0),
        registration_complete=True,
        current_day=1
    )
    return user.id if user else 0


async def After_Init(message: Message, context: FSMContext, db: DatabaseManager):
    """Called after initialization is complete."""
    # Placeholder for any post-init logic
    logger.info("Инициализация завершена")


async def START_LIFE(message: Message, context: FSMContext, db: DatabaseManager):
    """Show START1 block for existing users."""
    state_data = await context.get_data()
    user_name = state_data.get('user_nick', 'Игрок')
    logger.info(f"Пользователь: {user_name} прошел авторизацию")

    Update_step(19, context)
    message_text, keyboard, picture_path = Make_Block('START1')
    message_text = message_text.format(User_Name=user_name)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context, message)


async def START_PRO(message: Message, context: FSMContext, db: DatabaseManager):
    """Show START2 (professional/game start)."""
    await START_PRO2(message, context, db)


async def START_PRO2(message: Message, context: FSMContext, db: DatabaseManager):
    """Display START2 block."""
    await SEX_PRO('START2', context, message)


async def Start_ROLES(message: Message, context: FSMContext, db: DatabaseManager):
    """Show user status page (LB_STATUS)."""
    Update_step(19, context)
    user_live = get_credos(1)

    if await END_DAY(message, context, db):
        return

    FILL_UP = '\n📗 *Заполнить* _Дневник Осознанности_ 👉 /daily'
    user_role = get_role()
    message_text, keyboard, picture_path = Make_Block('LB_STATUS')
    user_vita = get_credos(2)
    day = Get_User_Day(context)

    dpas = await context.get_data()
    dpas = dpas.get('day_pass', '0')
    geoday = int(dpas) + 1

    week = get_uweek()
    dole = get_credos(4)
    user_refs = get_ref_count()
    ref_code = get_ref_code()
    taskflags = Check_user_flags(day)
    uf_ALL_fin = Is_ALL_fin(day, taskflags)
    status = jet_status(context)
    User_Rating = get_rating()
    ref_link = Comb_Reflink(ref_code)
    await context.update_data(user_reflink=ref_link)
    fillup = '' if uf_ALL_fin else FILL_UP
    leftday = MAX_DAYS - day
    leftdays = pluralize_ru(leftday, "день", "дня", "дней")

    message_text = message_text.format(
        User_Role=user_role,
        User_Rating=User_Rating,
        User_Live=user_live,
        geoday=geoday,
        maxday=MAX_DAYS,
        status=status,
        fillup=fillup,
        day=day,
        dole=dole,
        leftday=leftdays,
        week=week,
        wday=geoday  # Added for compatibility
    )
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context, message)


async def FINALIZE(message: Message, context: FSMContext, db: DatabaseManager) -> bool:
    """Check if user has reached the final day."""
    day = Get_User_Day(context)
    if day < MAX_DAYS:
        return False

    await SEX_PRO('FINAL', context, message)
    return True


async def END_DAY(message: Message, context: FSMContext, db: DatabaseManager) -> bool:
    """Check if day/game should end."""
    user_live = get_credos(1)
    if user_live and user_live <= 0:
        await END_book(context)
        return True
    else:
        await TUNE_DAY(context)
        return await FINALIZE(message, context, db)


async def TUNE_DAY(context: FSMContext):
    """Daily cron check."""
    INCRES = CRON_AMBA1(context)
    logger.info(f"ЧЕКАЕМ КРОНы 1-INCRES> {INCRES}")
    FLAG_CELC = CRON_AMBA2(context)
    logger.info(f"ЧЕКАЕМ КРОНы 2-CELC> {FLAG_CELC}")


async def START_BOOK(message: Message, context: FSMContext, db: DatabaseManager):
    """Start book (LB_START)."""
    await START_BOOKIN(message, context, db)


async def START_BOOKIN(message: Message, context: FSMContext, db: DatabaseManager):
    """Display LB_START block."""
    if await END_DAY(message, context, db):
        return

    pays = get_pays()
    User_Tarif = User_Tarifes[pays] if pays < len(User_Tarifes) else User_Tarifes[0]
    message_text, keyboard, picture_path = Make_Block('LB_START')
    message_text = message_text.format(User_Tarif=User_Tarif)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context, message)


async def START_INVEST(message: Message, context: FSMContext, db: DatabaseManager):
    """Show investment page."""
    preme = Get_User_Tarife(get_pays())
    dole, vita = get_credos(4), get_credos(2)
    message_text, keyboard, picture_path = Make_Block('INVEST')
    message_text = message_text.format(preme=preme, dole=dole, User_Vita=vita)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context, message)


async def GO_SHOP(message: Message, context: FSMContext, db: DatabaseManager):
    """Show shop."""
    await SEX_PRO('LB_SHOP', context, message)


async def START_NEW(message: Message, context: FSMContext, db: DatabaseManager):
    """Start new (LB_START)."""
    await SEX_PRO('LB_START', context, message)


async def START_DAY(message: Message, context: FSMContext, db: DatabaseManager):
    """Start daily tasks (LB_DAILY)."""
    if await END_DAY(message, context, db):
        return

    message_text, keyboard, picture_path = Make_Block('LB_DAILY')
    new_keyb = await Send_Task_Buttons(message, context, db)
    Block_PAK = message_text, new_keyb, picture_path
    await SEX_PROD(Block_PAK, context, message)


async def INPAY(message: Message, context: FSMContext, db: DatabaseManager):
    """Handle payment initiation."""
    state_data = await context.get_data()
    Moderator_ID = state_data.get('MOD_ID')
    text = "Игрок перешел к ОПЛАТЕ входа ПРОФИ"
    prepay_text = Prep_MOC4(context) + '\n' + text

    await SEX(prepay_text, context, message, FORMAT='B', SENDER=Moderator_ID)
    MSG = await SEX(prepay_text, context, message, FORMAT='B', SENDER=PAY_CHAT_id)

    await context.update_data(
        mid_Start_Text=prepay_text,
        mid_Start_Rules=MSG.message_id if MSG else None
    )
    logger.info(f'Записано mid_Start_Rules={MSG.message_id if MSG else None}')

    await SEX_PRO('LB_PAKET', context, message)


async def IN_TARIF(tarr: int, message: Message, context: FSMContext, db: DatabaseManager):
    """Handle tariff selection."""
    from utils import get_tariff_infoby_index

    state_data = await context.get_data()
    Moderator_ID = state_data.get('MOD_ID')
    price, vitas, lives = get_tariff_infoby_index(tarr - 1)
    tarif = f'`{price}` USDT' if tarr > 0 else ''

    await context.update_data(user_tarif=tarr)
    text = f"Игрок выбрал {tarr} ТАРИФ - {tarif}"
    prepay_text = Prep_MOC4(context) + '\n' + text

    MSG = state_data.get('mid_Start_Rules')
    text_full = state_data.get('mid_Start_Text', '') + '\n' + text
    await context.update_data(mid_Start_Text=text_full)

    if MSG:
        await SEX(text_full, context, message, FORMAT='B', EDIT=MSG, SENDER=PAY_CHAT_id)
    else:
        MSG = await SEX(prepay_text, context, message, FORMAT='B', SENDER=PAY_CHAT_id)
        await context.update_data(mid_Start_Rules=MSG.message_id if MSG else None)

    message_text, keyboard, picture_path = Make_Block('LB_INPAY')
    message_text = message_text.format(tar=tarr, payment=tarif)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context, message)


async def INPAIMENT(message: Message, context: FSMContext, db: DatabaseManager):
    """Handle payment confirmation request."""
    state_data = await context.get_data()
    Moderator_ID = state_data.get('MOD_ID')
    text = 'Для подтверждения оплаты нужен *чек или квитанция* об оплате\n_Отправьте чек в чат в виде изображения или PDF документа_'
    user_text = '*Уважаемый участник!*\n' + text
    await SEX(user_text, context, message, FORMAT='B')

    text = 'Игрок ☑️ Отправляет квитанцию'
    prepay_text = Prep_MOC4(context) + '\n' + text
    text2 = state_data.get('mid_Start_Text', '') + '\n' + text
    MSG = state_data.get('mid_Start_Rules')

    if MSG:
        MSG2 = await SEX(text2, context, message, FORMAT='B', EDIT=MSG, SENDER=PAY_CHAT_id)
    else:
        MSG2 = await SEX(prepay_text, context, message, FORMAT='B', SENDER=PAY_CHAT_id)

    Update_step(9, context)


async def INPAID(message: Message, context: FSMContext, db: DatabaseManager):
    """Handle payment receipt confirmation."""
    state_data = await context.get_data()
    text = 'Игрок ✅ Отправил квитанцию'
    prepay_text = Prep_MOC4(context) + '\n' + text
    MSG = state_data.get('mid_Start_Rules')

    if MSG:
        text3 = state_data.get('mid_Start_Text', '') + '\n' + text
        MSG2 = await SEX(text3, context, message, FORMAT='B', EDIT=MSG, SENDER=PAY_CHAT_id)
        await context.update_data(mid_Start_Text=text3)
    else:
        MSG2 = await SEX(prepay_text, context, message, FORMAT='B', SENDER=PAY_CHAT_id)

    logger.info(f'Репорт MSG={MSG2}')
    if MSG2:
        logger.info(f'Репорт MSGid={MSG2.message_id}')
        chat_id = str(PAY_CHAT_id).replace('-100', '')
        message_link = f"https://t.me/c/{chat_id}/{MSG2.message_id}"
        logger.info(f'Репорт MSG LINK={message_link}')

        text, keyboard = Prep_MOC5(message_link, context)
        await SEMOD(text, keyboard, context)

    mess = f'*Благодарим за оплату!*\nОжидайте подтверждения о получении перевода!\n_Проверка проходит в ручном режиме, поэтому может потребоваться немного времени_'
    await SEX(mess, context, message, FORMAT='B')

    Sdelay(3)
    await START_BOOKIN(message, context, db)


async def FILL_DAY(message: Message, context: FSMContext, db: DatabaseManager):
    """Show day completion bonus."""
    state_data = await context.get_data()
    user_name = state_data.get('user_nick', 'Игрок')
    dole = get_credos(4)
    message_text, keyboard, picture_path = Make_Block('LB_BONUS')
    message_text = message_text.format(name=user_name, maxday=MAX_DAYS)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context, message)


# ===== PARTNER INTEGRATION FUNCTIONS =====

async def DONNA_SET(message: Message, context: FSMContext, db: DatabaseManager):
    """Set DONNA partner link."""
    await SEX('Задайте свою *партнерскую ссылку проекта DONNA* для приглашения друзей.\n_Для этого ▶️ отправьте в чат Вашу реферальную ссылку проекта_ *Donna AI* 👇🏻', context, message, FORMAT='B')
    Update_step(11, context)


async def UNI_SET(message: Message, context: FSMContext, db: DatabaseManager):
    """Set UNILIVE partner link."""
    await SEX('Задайте свою *партнерскую ссылку проекта UNILIVE* для приглашения друзей.\n_Для этого ▶️ отправьте в чат Вашу реферальную ссылку проекта_ *UniLIVE* 👇🏻', context, message, FORMAT='B')
    Update_step(18, context)


async def AXI0_SET(message: Message, context: FSMContext, db: DatabaseManager):
    """Set AXIOMA partner login."""
    await SEX('Задайте свой *партнерский логин проекта AXIOMA* для приглашения друзей.\n_Для этого ▶️ отправьте в чат Ваш партнерский логин проекта_ *AXIOMA* 👇🏻', context, message, FORMAT='B')
    Update_step(21, context)


async def AXI5_SET(message: Message, context: FSMContext, db: DatabaseManager):
    """Set LIFE5 partner link."""
    await SEX('Задайте свою *партнерскую ссылку проекта LIFE5* для приглашения друзей.\n_Для этого ▶️ отправьте в чат Вашу реферальную ссылку проекта_ *LIFE5* 👇🏻', context, message, FORMAT='B')
    Update_step(22, context)


async def DONNA_RUN(message: Message, context: FSMContext, db: DatabaseManager):
    """Show DONNA integration."""
    await DONNA(message, context, db)


async def DONNA(message: Message, context: FSMContext, db: DatabaseManager):
    """Display DONNA partner page."""
    donna_url = Get_DONNA_URL()
    message_text, keyboard, picture_path = Make_Block('LP_DONNA')
    message_text = message_text.format(donna_url=donna_url)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context, message)


async def UNI_RUN(message: Message, context: FSMContext, db: DatabaseManager):
    """Show UNILIVE integration."""
    await UNILIVE(message, context, db)


async def UNILIVE(message: Message, context: FSMContext, db: DatabaseManager):
    """Display UNILIVE partner page."""
    uni_url = Get_UNI_URL()
    message_text, keyboard, picture_path = Make_Block('LP_UNI')
    message_text = message_text.format(uni_url=uni_url)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context, message)


async def AXIOM5_RUN(message: Message, context: FSMContext, db: DatabaseManager):
    """Show AXIOM5/5LIFE integration."""
    await AXIOM5(message, context, db)


async def AXIOM5(message: Message, context: FSMContext, db: DatabaseManager):
    """Display 5LIFE partner page."""
    axi5_url = Get_AXI5M_URL()
    message_text, keyboard, picture_path = Make_Block('LP_5LIFE')
    message_text = message_text.format(axi5_url=axi5_url)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context, message)


async def AXIOM0_RUN(message: Message, context: FSMContext, db: DatabaseManager):
    """Show AXIOM integration."""
    await AXIOM0(message, context, db)


async def AXIOM0(message: Message, context: FSMContext, db: DatabaseManager):
    """Display AXIOM partner page."""
    from const import AXIOM_URL
    message_text, keyboard, picture_path = Make_Block('LP_AXIOM')
    message_text = message_text.format(axi0_url=AXIOM_URL)
    Block_Pk = message_text, keyboard, picture_path
    await SEX_PROD(Block_Pk, context, message)


# ===== HOMEWORK AND PROGRESS FUNCTIONS =====

async def TEST_HOMEJOB(message: Message, context: FSMContext, db: DatabaseManager) -> bool:
    """Test if homework is complete and award bonuses."""
    day = Get_User_Day(context)
    taskflags = Check_user_flags(day)
    uf_ALL_fin = Is_ALL_fin(day, taskflags)

    dole_FP = Get_DOLE_FP()
    logger.info(f'>>>>>>>>>>> dole_FP={dole_FP}')
    subflag = False

    if uf_ALL_fin:  # All 3 tasks complete
        if not dole_FP:  # Haven't awarded bonus yet
            subflag = True
            await FILL_DAY(message, context, db)
            await INC_DOLE(message, context, db)
            Set_DOLE_FP(True)
            await Adelay(1)

        week = get_uweek()
        if await WEEK_SHOW(week, message, context, db):
            subflag = True

        if subflag:
            return False

    return True  # need to return to START


async def TEST_EVENING(message: Message, context: FSMContext, db: DatabaseManager) -> bool:
    """Evening check - verify homework and progress day."""
    day = Get_User_Day(context)
    taskflags = Check_user_flags(day)
    uf_ANY_fin = Is_ANY_fin(day, taskflags)
    uf_ALL_fin = Is_ALL_fin(day, taskflags)
    message_txt = ">🧑🏻‍🎓> Проверка домашнего задания:"
    mesfin = "\n💤 НАЧАТЬ НОВЫЙ ДЕНЬ ▶️ /start"

    if uf_ALL_fin:  # All 3 tasks complete
        await Inc_Day(context)
        logger.info("Был переход дня")
        Set_DOLE_FP(False)
        logger.info("Обновлен триггер ДОЛИ")
        warn = f'{message_txt} OK ✅\nВсе задания выполнены, происходит прогресс дня{mesfin}'
        await START_AGAIN(warn, message, context, db)
        return True

    if uf_ANY_fin:  # At least 1 task complete
        warn = f'{message_txt} OK ☑️\nНе все задания выполнены, нет прогресса марафона {mesfin}'
        await START_AGAIN(warn, message, context, db)
        return False

    LIVES = get_credos(1)
    if LIVES > 0:
        LIVES -= 1
    save_credos(1, LIVES)

    await SEX(f'{message_txt} НЕ ВЫПОЛНЕНО ❌\n- Вы теряете 1❤️, осталось: {LIVES}❤️ {mesfin}', context, message)

    if LIVES <= 0:
        await END_book(context)
        return False

    return False


async def WEEKJOB(message: Message, context: FSMContext, db: DatabaseManager):
    """Weekly job - award bonuses and generate report."""
    await Inc_Lives(context, lives=1)
    await Inc_Vitas(context, vitas=1)
    await SEX('НЕДЕЛЬНЫЙ ОТЧЕТ: награды получены, ждем ответ от Фрейи', context, message)
    await FREYA_WEEK(context)
    week = get_uweek()
    save_uweek(week + 1)
    await TEST_MONTH(message, context, db)


async def TEST_MONTH(message: Message, context: FSMContext, db: DatabaseManager):
    """Check if month/marathon is complete."""
    day = Get_User_Day(context)
    if day == MAX_DAYS:
        user_progress()
        await Inc_Lives(context, lives=5)
        await Inc_Vitas(context, vitas=10)

    if day > MAX_DAYS:
        day = 1
        save_day(day)


async def INC_DOLE(message: Message, context: FSMContext, db: DatabaseManager):
    """Increment daily progress counter."""
    dole = get_credos(4)
    dole += 1

    if dole == 7:
        await WEEKJOB(message, context, db)

    if dole > 7:
        dole = 1

    save_credos(4, dole)


async def WEEK_SHOW(week: int, message: Message, context: FSMContext, db: DatabaseManager) -> bool:
    """Show weekly promo/bonus."""
    if week == 1:
        return await Promo_Show(message, context, db)
    if week == 2:
        return await Promo_Donna(message, context, db)
    return False


async def Promo_Show(message: Message, context: FSMContext, db: DatabaseManager) -> bool:
    """Show first week bonus."""
    show_FP = Get_SHOW_FP()
    if not show_FP:
        await MORE_BONUS(message, context, db)
        Set_SHOW_FP(True)
        return True
    return False


async def Promo_Donna(message: Message, context: FSMContext, db: DatabaseManager) -> bool:
    """Show DONNA promo on week 2."""
    donna_FP = Get_DONNA_FP()
    if not donna_FP:
        await DONNA(message, context, db)
        Set_DONNA_FP(True)
        return True
    return False


async def MORE_BONUS(message: Message, context: FSMContext, db: DatabaseManager):
    """Show more bonus block."""
    await SEX_PRO('MORE_BONUS', context, message)


async def MORE_INFO(message: Message, context: FSMContext, db: DatabaseManager):
    """Show more info block."""
    await SEX_PRO('MORE_INFO', context, message)


async def Send_Task_Buttons(message: Message, context: FSMContext, db: DatabaseManager):
    """Generate task buttons for daily tasks."""
    day = Get_User_Day(context)
    taskflags = Check_user_flags(day)
    buttons = []

    for i, task in enumerate(TASKS):
        if i < N_TAX:
            textbut = f"{task}"
            if taskflags[i]:
                textbut = textbut + " ✅"
            callback = f"hometask_{i}"
            buttons.append([InlineKeyboardButton(text=textbut, callback_data=callback)])

    textback = "Выйти"
    buttons.append([InlineKeyboardButton(text=textback, callback_data='start_new')])
    return Make_KEYB(buttons)


async def Ask_TZ(message: Message, context: FSMContext, db: DatabaseManager):
    """Ask for timezone selection."""
    await context.update_data(mid_Ask_Zone=None)
    Update_step(13, context)
    await Ask_ZONE(context)


# ===== BUTTON CALLBACK HANDLER =====

async def BUTTON_RUN(callback: CallbackQuery, context: FSMContext, db: DatabaseManager):
    """Main callback handler for button presses."""
    data = callback.data
    message = callback.message

    logger.info(f"Button pressed: {data}")

    # Registration flow
    if data == "registration":
        await START_JOIN2(message, context, db)

    # Role selection
    elif data.startswith("setrole_"):
        role_idx = int(data.split("_")[1])
        await SETUP_ROLE(role_idx, message, context, db)

    # Game flow
    elif data == "start_pro":
        await START_PRO(message, context, db)
    elif data == "begin_game":
        await Start_ROLES(message, context, db)
    elif data == "life_book":
        await START_BOOK(message, context, db)
    elif data == "start_day":
        await START_DAY(message, context, db)
    elif data == "start_new":
        await START_NEW(message, context, db)

    # Freya AI
    elif data == "freya_run":
        # Handle Freya AI assistant
        pass

    # Partner integrations
    elif data == "donna_run":
        await DONNA_RUN(message, context, db)
    elif data == "uni_run":
        await UNI_RUN(message, context, db)
    elif data == "axiom_run":
        await AXIOM0_RUN(message, context, db)
    elif data == "axi5_run":
        await AXIOM5_RUN(message, context, db)

    # Task buttons
    elif data.startswith("hometask_"):
        task_id = int(data.split("_")[1])
        # Handle task selection
        pass

    # Payment flow
    elif data.startswith("tarif_"):
        tariff = int(data.split("_")[1])
        await IN_TARIF(tariff, message, context, db)
    elif data == "inpay":
        await INPAY(message, context, db)
    elif data == "inpaiment":
        await INPAIMENT(message, context, db)

    # Acknowledge callback
    await callback.answer()


async def INPUT_RUN(message: Message, context: FSMContext, db: DatabaseManager):
    """Main text input handler."""
    state_data = await context.get_data()
    step = state_data.get('step', 0)

    logger.info(f"Text input at step: {step}")

    # Step 1: Nickname input (JOIN2)
    if step == 1:
        await START_JOIN2_GOT(message.text, message, context, db)

    # Add other step handlers as needed
    else:
        logger.info(f"Unhandled text input at step {step}: {message.text}")


# Export main functions
__all__ = [
    'START_AGAIN', 'START_JOIN', 'START_LIFE', 'START_PRO',
    'START_BOOK', 'START_DAY', 'Start_ROLES', 'BUTTON_RUN', 'INPUT_RUN',
    'GLUBDATE', 'DONNA', 'UNILIVE', 'AXIOM0', 'AXIOM5',
    'TEST_HOMEJOB', 'TEST_EVENING'
]
