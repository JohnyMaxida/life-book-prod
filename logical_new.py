"""
Новый корневой логический движок (orchestrator).
Использует блоковую систему UI из lifeBlock.py через ui_blocks.py
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
    send_block,
    get_life_block,
    get_life_block_titles,
    format_block_text,
    create_menu_from_block
)
from const import MAX_DAYS

# Настройка логирования
logger = logging.getLogger(__name__)

# Константы
TASKS = [
    "Радость дня 😊",
    "Благодарность дня 🙏",
    "❓ Вопрос дня 💡"
]

class BotFlow:
    """Класс для управления основными потоками бота."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.block_mapping = {
            'JOIN1': 'JOIN1',
            'JOIN2': 'JOIN2',
            'JOIN3': 'JOIN3',
            'JOIN4': 'JOIN4',
            'FINAL': 'FINAL',
            'LB_START': 'LB_START',
            'LB_STATUS': 'LB_STATUS',
            'LB_DAILY': 'LB_DAILY',
            'REFER': 'REFER',
            'REFER_FULL': 'REFER_FULL',
            'INVEST': 'INVEST',
            'LB_PAKET': 'LB_PAKET',
            'LB_INPAY': 'LB_INPAY',
            'LB_BONUS': 'LB_BONUS',
            'MORE_BONUS': 'MORE_BONUS',
            'MORE_INFO': 'MORE_INFO',
            'RESET_WARN': 'RESET_WARN'
        }
    
    async def start_flow(self, message: Message, state: FSMContext) -> None:
        """Обработка команды /start."""
        user_id = message.from_user.id
        
        # Проверяем, новый ли пользователь
        user = await self.db.get_user(user_id)
        if not user:
            # Новый пользователь - показываем приветствие
            await self._handle_new_user_flow(message, state)
        else:
            # Существующий пользователь - показываем главное меню
            await self._show_main_menu(message, state)
    
    async def _handle_new_user_flow(self, message: Message, state: FSMContext) -> None:
        """Обработка потока для нового пользователя."""
        # Показываем приветственный блок
        await self._send_block('JOIN1', message, state)
        
        # Устанавливаем состояние ожидания имени
        await state.set_state("waiting_for_name")
    
    async def _show_main_menu(self, message: Message, state: FSMContext) -> None:
        """Показать главное меню."""
        user_id = message.from_user.id
        user = await self.db.get_user(user_id)
        
        # Определяем, какой блок показать в зависимости от дня
        if user.current_day > MAX_DAYS:
            await self._send_block('FINAL', message, state)
        else:
            await self._send_block('LB_START', message, state, {
                'User_Name': user.username or 'Игрок',
                'day': user.current_day,
                'max_day': MAX_DAYS
            })
    
    async def handle_text_input(self, message: Message, state: FSMContext) -> None:
        """Обработка текстового ввода пользователя."""
        current_state = await state.get_state()
        
        if current_state == "waiting_for_name":
            await self._process_user_name(message, state)
        # Добавьте другие состояния по мере необходимости
    
    async def _process_user_name(self, message: Message, state: FSMContext) -> None:
        """Обработка введенного имени пользователя."""
        user_name = message.text.strip()
        
        # Сохраняем имя пользователя
        user_id = message.from_user.id
        await self.db.update_user(user_id, {"username": user_name})
        
        # Показываем следующий блок с выбором роли
        await self._send_block('JOIN3', message, state, {
            'User_Name': user_name
        })
        
        # Меняем состояние на ожидание выбора роли
        await state.set_state("waiting_for_role")
    
    async def handle_callback(self, callback: CallbackQuery, state: FSMContext) -> None:
        """Обработка callback-запросов от кнопок."""
        data = callback.data
        
        # Обработка нажатий на кнопки
        if data == "start_game":
            await self._start_game(callback, state)
        elif data == "show_status":
            await self._show_status(callback, state)
        elif data == "begin_game":
            await self._show_main_menu(callback.message, state)
        elif data == "start_day":
            await self._start_day(callback.message, state)
        elif data == "refer_menu":
            await self._show_referral_menu(callback.message, state)
        elif data == "invest_menu":
            await self._show_invest_menu(callback.message, state)
        # Добавьте другие обработчики кнопок
    
    async def _start_game(self, callback: CallbackQuery, state: FSMContext) -> None:
        """Начать игру (обработка нажатия на кнопку старта)."""
        user_id = callback.from_user.id
        
        # Обновляем статус пользователя
        await self.db.update_user(user_id, {"status": "active"})
        
        # Показываем первый день
        await self._show_day_content(callback.message, 1)
        
        await callback.answer()
    
    async def _show_status(self, callback: CallbackQuery, state: FSMContext) -> None:
        """Показать статус пользователя."""
        user_id = callback.from_user.id
        user = await self.db.get_user(user_id)
        
        # Формируем текст статуса
        status_text = (
            f"📊 *Ваш статус*\n"
            f"День: {user.current_day}/{MAX_DAYS}\n"
            f"Очков: {user.points}\n"
            f"Жизни: {user.lives}"
        )
        
        # Отправляем статус
        await callback.message.answer(status_text, parse_mode="MarkdownV2")
        await callback.answer()
    
    async def _show_day_content(self, message: Message, day: int) -> None:
        """Показать контент для указанного дня."""
        user_id = message.from_user.id
        user = await self.db.get_user(user_id)
        
        # Показываем блок с днем
        await self._send_block('LB_DAILY', message, None, {
            'day': day,
            'max_day': MAX_DAYS,
            'User_Name': user.username or 'Игрок'
        })
        
        # Показываем задачи на день
        await self._show_tasks(message, day)
    
    async def _show_tasks(self, message: Message, day: int) -> None:
        """Показать задачи на день."""
        # Получаем блок с задачами
        block = get_life_block("TASKS")
        if not block:
            return
        
        # Форматируем текст с задачами
        tasks_text = "\n".join([f"{i+1}. {task}" for i, task in enumerate(TASKS)])
        text = format_block_text(block, day=day, tasks=tasks_text)
        
        # Создаем клавиатуру с задачами
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=task, callback_data=f"task_{i}")] 
            for i, task in enumerate(TASKS)
        ])
        
        # Отправляем сообщение
        await message.answer(text, reply_markup=keyboard, parse_mode="MarkdownV2")
        
    async def _show_referral_menu(self, message: Message, state: FSMContext) -> None:
        """Показать меню реферальной программы."""
        user_id = message.from_user.id
        user = await self.db.get_user(user_id)
        
        # Получаем реферальную информацию
        ref_count = await self.db.get_referral_count(user_id)
        ref_code = user.referral_code or f"ref{user_id}"
        ref_link = f"https://t.me/your_bot_username?start={ref_code}"
        
        await self._send_block('REFER', message, state, {
            'name': user.username or 'Игрок',
            'ref_cont': ref_count,
            'ref_code': ref_code,
            'ref_link': ref_link
        })
    
    async def _show_invest_menu(self, message: Message, state: FSMContext) -> None:
        """Показать меню инвестиций."""
        user_id = message.from_user.id
        user = await self.db.get_user(user_id)
        
        await self._send_block('INVEST', message, state, {
            'preme': 'Активен' if user.is_premium else 'Не активен',
            'dole': user.premium_days if user.is_premium else 0,
            'User_Vita': user.vita_points or 0
        })
    
    async def _start_day(self, message: Message, state: FSMContext) -> None:
        """Начать новый день."""
        user_id = message.from_user.id
        user = await self.db.get_user(user_id)
        
        # Проверяем, можно ли начать новый день
        if user.current_day > MAX_DAYS:
            await self._send_block('FINAL', message, state)
            return
            
        # Показываем контент дня
        await self._show_day_content(message, user.current_day)
    
    async def _send_block(self, block_name: str, message: Message, state: FSMContext, format_vars: dict = None) -> bool:
        """Отправить блок из lifeBlock.py."""
        from ui_blocks import get_block, format_block_text, create_menu_from_block, SEX
        
        if not format_vars:
            format_vars = {}
            
        # Добавляем стандартные переменные
        user_id = message.from_user.id
        user = await self.db.get_user(user_id)
        
        # Get the block from lifeBlock
        block = get_block(block_name)
        if not block:
            logger.error(f"Block '{block_name}' not found")
            return False
            
        # Format the block text with provided variables
        text = format_block_text(block, **format_vars)
        
        # Create keyboard from block menu
        keyboard = create_menu_from_block(block)
        
        # Ensure keyboard is in the correct format
        if keyboard and hasattr(keyboard, 'inline_keyboard'):
            keyboard = keyboard.inline_keyboard
        
        # Send the message with the block content
        await SEX(
            text=text,
            context=message,
            SENDER=user_id,
            MENU=keyboard,
            FORMAT='B'  # MarkdownV2 formatting
        )
        return True

# Функции для работы с кронами
async def evening_check_flow(bot: Bot, db_manager: DatabaseManager) -> None:
    """Вызывается по крону в 18:00 — проверяет ДЗ и даёт анализ."""
    # Получаем всех активных пользователей
    users = await db_manager.get_active_users()
    
    for user in users:
        try:
            # Проверяем выполнение заданий
            completed = await check_homework(user)
            
            if completed:
                # Обновляем прогресс
                await inc_day_if_complete(user, db_manager)
                
                # Проверяем конец недели/марафона
                if is_week_end(user):
                    await handle_week_end(user, bot, db_manager)
                
                if is_final_day(user):
                    await generate_and_send_report(user, bot, db_manager, final=True)
            
            # Отправляем вечерний анализ
            await run_evening_analysis(user, bot, db_manager)
            
        except Exception as e:
            logger.error(f"Error in evening check for user {user.id}: {e}")

async def daily_reminder_flow(bot: Bot, db_manager: DatabaseManager) -> None:
    """Вызывается по крону в 14:00 — напоминает о незаполненных ответах."""
    users = await db_manager.get_users_with_incomplete_tasks()
    
    for user in users:
        try:
            await bot.send_message(
                chat_id=user.id,
                text="⏰ Не забудьте выполнить задания за сегодня!"
            )
        except Exception as e:
            logger.error(f"Error sending reminder to {user.id}: {e}")

async def weekly_report_flow(bot: Bot, db_manager: DatabaseManager) -> None:
    """Вызывается после завершения недели — недельный отчёт + бонусы."""
    users = await db_manager.get_weekly_completers()
    
    for user in users:
        try:
            # Генерируем и отправляем отчет
            await generate_and_send_report(user, bot, db_manager)
            
            # Начисляем бонусы
            await db_manager.update_user(user.id, {"points": user.points + 50})
            
            # Уведомляем пользователя
            await bot.send_message(
                chat_id=user.id,
                text="🎉 Поздравляем с завершением недели! Вам начислено 50 бонусных очков!"
            )
            
        except Exception as e:
            logger.error(f"Error in weekly report for user {user.id}: {e}")
