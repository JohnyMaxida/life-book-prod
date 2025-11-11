"""
LIFEBOOK - Telegram бот для марафона самопознания
Версия с чистой архитектурой на aiogram 3.x
"""
import asyncio
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# Импорты новой архитектуры
from db_manager import DatabaseManager, get_db
from command_handlers import setup_handlers, init_command_handlers
from config import config as settings
from logger import logger  # Централизованный логгер
from const import MAX_DAYS, MAX_STIX, ITEMS_PER_PAGE, LOG_LIM

class AppConfig:
    """Конфигурация приложения"""
    def __init__(self):
        self.VERSION = "1.0.0"
        self.DEBUG = settings.debug
        
        # Пути
        self.BASE_DIR = Path(__file__).parent
        self.DATA_DIR = self.BASE_DIR / "DATA-LIFE"
        self.ART_DIR = self.DATA_DIR / "life-art"
        self.ARTBLOCK_DIR = self.DATA_DIR / "art-block"
        self.LOGS_DIR = self.BASE_DIR / "logs"
        
        # Создаем необходимые директории
        self.DATA_DIR.mkdir(exist_ok=True)
        self.ART_DIR.mkdir(exist_ok=True)
        self.ARTBLOCK_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)
        
        # Настройки бота
        # Get token directly from environment first, then fall back to config
        self.BOT_TOKEN = os.getenv('LB_BOT__TOKEN_TEST') or (
            settings.bot.token_server if settings.bot.get('production', False) 
            else settings.bot.token_test
        )
        
        # Ensure token is not empty
        if not self.BOT_TOKEN:
            logger.critical("Bot token is not set! Please check your .env file")
            sys.exit(1)
            
        # Convert admin IDs to list of integers
        admin_ids = os.getenv('LB_BOT__ADMIN_IDS', '').strip('[]')
        self.ADMIN_IDS = [int(x.strip()) for x in admin_ids.split(',') if x.strip().isdigit()]
        
        # Fallback to config if no admin IDs in environment
        if not self.ADMIN_IDS and hasattr(settings.bot, 'admin_ids'):
            self.ADMIN_IDS = settings.bot.admin_ids
        
        # Режимы работы
        self.IS_PRODUCTION = settings.bot.get('production', False)
        self.IS_DEMO = settings.bot.get('demo_mode', False)

# Инициализация конфигурации
app_config = AppConfig()

# Access admin and chat configuration
MODERATORS = settings.admins.moderators
ADMINS = settings.admins.admins
REVISORS = settings.admins.revisors

# Chat IDs
LIFE_CHAT_ID = settings.chats.life_chat_id
PAY_CHAT_id = settings.chats.pay_chat_id
DEV_CHAT_id = settings.chats.dev_chat_id

async def button_callback_handler(query: types.CallbackQuery) -> None:
    """Обработчик нажатий на инлайн-кнопки"""
    user = query.from_user
    data = query.data
    
    logger.info(f"Нажата кнопка пользователем {user.id} ({user.full_name}): {data}")
    
    # Подтверждаем нажатие кнопки
    await query.answer()
    
    # Здесь будет логика обработки нажатий на кнопки
    response = f"Вы нажали кнопку: {data}"
    
    await query.message.edit_text(response)

async def audio_message_handler(message: types.Message) -> None:
    """Обработчик аудиосообщений"""
    user = message.from_user
    logger.info(f"Получено аудиосообщение от {user.id} ({user.full_name})")
    await message.answer("Спасибо за аудиосообщение!")

async def video_message_handler(message: types.Message) -> None:
    """Обработчик видеосообщений"""
    user = message.from_user
    logger.info(f"Получено видеосообщение от {user.id} ({user.full_name})")
    await message.answer("Спасибо за видеосообщение!")

async def main() -> None:
    """Главная функция запуска бота"""
    logger.info(f"Инициализация бота...")
    logger.info(f"Версия: {app_config.VERSION}")
    logger.info(f"Режим: {'PRODUCTION' if app_config.IS_PRODUCTION else 'DEVELOPMENT'}")
    
    try:
        # Инициализация бота и диспетчера
        from aiogram.client.default import DefaultBotProperties
        bot = Bot(
            token=app_config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode='HTML')
        )
        dp = Dispatcher(storage=MemoryStorage())  # Use MemoryStorage for FSM
        
        # Инициализация базы данных
        logger.info("Инициализация базы данных...")
        database = await get_db()
        
        # Регистрация обработчиков
        logger.info("Регистрация обработчиков...")
        setup_handlers(dp, database)
        
        # Регистрация обработчиков сообщений, которые не в command_handlers
        dp.callback_query.register(button_callback_handler)
        # Обработка только аудио в личных сообщениях
        dp.message.register(audio_message_handler, (F.audio | F.voice) & F.chat.type == 'private')
        # Видео хендлер отключен по запросу
        
        # Запуск бота
        logger.info(f"Бот запущен в режиме: {'PRODUCTION' if app_config.IS_PRODUCTION else 'DEVELOPMENT'}")
        
        # Запускаем поллинг
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            skip_updates=True
        )
        
    except asyncio.CancelledError:
        logger.info("Получен запрос на остановку бота")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}", exc_info=True)
        raise
    finally:
        if 'bot' in locals():
            await bot.session.close()
            logger.info("Сессия бота закрыта")
        logger.info("Бот остановлен")

if __name__ == '__main__':
    # Настройка обработки сигналов для корректного завершения
    import signal
    import sys
    
    # Обработчик сигнала прерывания (Ctrl+C)
    def handle_sigint(signum, frame):
        logger.info("Получен сигнал на завершение работы...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, handle_sigint)
    
    # Запуск приложения
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Приложение остановлено пользователем")
    except Exception as e:
        logger.critical(f"Непредвиденная ошибка: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Приложение завершило работу")
