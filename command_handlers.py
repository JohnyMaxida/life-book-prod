"""
Command Handlers Module

This module handles all bot commands and callback queries using aiogram 3.x.
"""
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, Union, List

from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from const import MAX_DAYS
from db_manager import DatabaseManager
from ui_blocks import show_block, get_block, format_block_text, create_menu_from_block
from config import config as settings
from logger import logger as main_logger
from ui_blocks import (
    build_main_menu,
    build_profile_menu,
    build_settings_menu,
    build_help_menu,
    build_marathon_progress
)

# Configure logging
logger = logging.getLogger(__name__)

# Database instance will be set during initialization
db = None

# Initialize router
router = Router()

# States for registration
class RegistrationStates(StatesGroup):
    awaiting_nickname = State()
    awaiting_join2 = State()
    awaiting_join3 = State()
    awaiting_join4 = State()
    registration_complete = State()

class CommandHandlers:
    """Handles all bot commands and callbacks."""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        if not self.db:
            raise ValueError("Database manager instance is required")
            
        self.commands = {
            'start': self.handle_start,
            'help': self.handle_help,
            'profile': self.handle_profile,
            'progress': self.handle_daily,
            'settings': self.handle_settings,
            'daily': self.handle_daily,
            'referral': self.handle_referral,
            'admin': self.handle_admin,
            'status': self.handle_status,
            'shop': self.handle_shop,
            'invest': self.handle_invest,
            'donna': self.handle_donna,
            'unilive': self.handle_unilive,
            '5life': self.handle_5life,
            'axiom': self.handle_axiom,
            'feedback': self.handle_feedback,
            'freya': self.handle_freya
        }
        
        # Register handlers
        self._register_handlers()
        
        # Callback query handler
        router.callback_query()(self.process_callback)
        
        # Import UI blocks
        from ui_blocks import SEX_PRO, get_block, format_block_text, create_menu_from_block
    
    def _register_handlers(self) -> None:
        """Register all command and callback handlers."""
        # Command handlers
        router.message(CommandStart())(self.handle_start)
        router.message(Command('help'))(self.handle_help)
        router.message(Command('profile'))(self.handle_profile)
        router.message(Command('daily', 'progress'))(self.handle_daily)
        router.message(Command('settings'))(self.handle_settings)
        router.message(Command('referral'))(self.handle_referral)
        router.message(Command('admin'))(self.handle_admin)
        router.message(Command('status'))(self.handle_status)
        router.message(Command('shop'))(self.handle_shop)
        router.message(Command('invest'))(self.handle_invest)
        router.message(Command('donna'))(self.handle_donna)
        router.message(Command('unilive'))(self.handle_unilive)
        router.message(Command('5life'))(self.handle_5life)
        router.message(Command('axiom'))(self.handle_axiom)
        router.message(Command('feedback'))(self.handle_feedback)
        router.message(Command('freya'))(self.handle_freya)
        
        # Text message handlers
        router.message(
            F.text & ~F.command,
            StateFilter(RegistrationStates.awaiting_nickname)
        )(self.handle_nickname_input)
        
        # Callback query handlers
        router.callback_query(F.data.startswith('reset_'))(self.handle_reset_confirm)
        router.callback_query(F.data == 'begin_game')(self.handle_begin_game)
        router.callback_query(F.data == 'life_book')(self.handle_life_book)
    
    async def process_message(self, message: Message) -> None:
        """Process incoming message and route to appropriate handler."""
        if not message.text or not message.text.startswith('/'):
            return
            
        command = message.text.split('@')[0].lower().lstrip('/')
        handler = self.commands.get(command)
        if handler:
            try:
                await handler(message)
            except Exception as e:
                logger.error(f"Error processing command {command}: {e}")
                await self._send_error(message, "Произошла ошибка при обработке команды.")
    
    async def handle_start(self, message: Message, state: FSMContext) -> None:
        """Handle /start command - initial user interaction."""
        user = message.from_user
        
        try:
            if not hasattr(self, 'db') or self.db is None:
                logger.error("Database not initialized in handle_start")
                await message.answer("❌ Ошибка инициализации базы данных. Пожалуйста, попробуйте позже.")
                return
                
            # Check if user exists and has completed registration
            existing_user = await self.db.get_user(user.id)
            
            if not existing_user or not getattr(existing_user, 'registration_complete', False):
                # New user or not fully registered - start with JOIN1
                await show_block(message, 'JOIN1')
                await state.set_state(RegistrationStates.awaiting_join2)
                
                # Store user data in state
                user_data = {
                    'user_id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'current_join_block': 'JOIN1'
                }
                await state.update_data(**user_data)
                
                # Create or update user in database
                await self.db.get_or_create_user(
                    user_id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    registration_complete=False
                )
            else:
                # Existing user - show appropriate START block based on day
                await self._show_user_day(message, existing_user)
                
        except Exception as e:
            logger.error(f"Error in handle_start: {str(e)}", exc_info=True)
            await message.answer("❌ Произошла ошибка при обработке команды. Пожалуйста, попробуйте снова.")
            # Try to log the error to help with debugging
            try:
                logger.error(f"Database state - has_db: {hasattr(self, 'db')}, db_type: {type(getattr(self, 'db', None))}")
            except Exception as log_error:
                logger.error(f"Failed to log database state: {log_error}")
            
    async def handle_registration_message(self, message: Message, state: FSMContext) -> None:
        """Handle user messages during registration flow."""
        try:
            # Get current state data
            state_data = await state.get_data()
            current_block = state_data.get('current_join_block')
            
            if current_block == 'JOIN1':
                # Process JOIN1 response and show JOIN2
                await self._process_join1_response(message, state, state_data)
            elif current_block == 'JOIN2':
                # Process JOIN2 response and show JOIN3
                await self._process_join2_response(message, state, state_data)
            elif current_block == 'JOIN3':
                # Process JOIN3 response and show JOIN4
                await self._process_join3_response(message, state, state_data)
            elif current_block == 'JOIN4':
                # Process JOIN4 response and complete registration
                await self._complete_registration(message, state, state_data)
            else:
                # If we don't recognize the block, restart registration
                await message.answer("❌ Не удалось определить этап регистрации. Начинаем сначала.")
                await self.handle_start(message, state)
                
        except Exception as e:
            logger.error(f"Error in handle_registration_message: {str(e)}")
            await message.answer("❌ Произошла ошибка при обработке вашего ответа. Пожалуйста, попробуйте снова.")
            await self.handle_start(message, state)
            
    async def _process_join1_response(self, message: Message, state: FSMContext, state_data: dict) -> None:
        """Process user response to JOIN1 block."""
        # Store the response and show JOIN2
        await state.update_data({
            'join1_response': message.text,
            'current_join_block': 'JOIN2'
        })
        await self._show_block(message, 'JOIN2')
        await state.set_state('awaiting_join3')
        
    async def _process_join2_response(self, message: Message, state: FSMContext, state_data: dict) -> None:
        """Process user response to JOIN2 block."""
        # Store the response and show JOIN3
        await state.update_data({
            'join2_response': message.text,
            'current_join_block': 'JOIN3'
        })
        await self._show_block(message, 'JOIN3')
        await state.set_state('awaiting_join4')
        
    async def _process_join3_response(self, message: Message, state: FSMContext, state_data: dict) -> None:
        """Process user response to JOIN3 block."""
        # Store the response and show JOIN4
        await state.update_data({
            'join3_response': message.text,
            'current_join_block': 'JOIN4'
        })
        await self._show_block(message, 'JOIN4')
        await state.set_state('awaiting_registration_complete')
        
    async def _complete_registration(self, message: Message, state: FSMContext, state_data: dict) -> None:
        """Complete user registration and save to database."""
        # Store the final response
        await state.update_data({
            'join4_response': message.text,
            'registration_complete': True
        })
        
        # Get all registration data
        user_data = await state.get_data()
        
        # Save user to database
        user = await self.db.get_or_create_user(
            user_id=user_data['user_id'],
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            registration_data={
                'join1': user_data.get('join1_response'),
                'join2': user_data.get('join2_response'),
                'join3': user_data.get('join3_response'),
                'join4': user_data.get('join4_response')
            },
            registration_complete=True,
            current_day=1  # Start with day 1
        )
        
        # Clear the state
        await state.clear()
        
        # Show welcome message and first day content
        await message.answer("🎉 Регистрация завершена! Добро пожаловать!")
        await self._show_user_day(message, user)
    
    def _user_to_dict(self, user_obj):
        """Convert User object to dictionary."""
        if user_obj is None:
            return {}
        if isinstance(user_obj, dict):
            return user_obj
        return {k: v for k, v in user_obj.__dict__.items() if not k.startswith('_')}

    async def _show_user_day(self, message: Message, user_data) -> None:
        """Show the appropriate day content for existing user."""
        try:
            # Get user ID and current day
            user_id = user_data.id if hasattr(user_data, 'id') else user_data.get('id')
            current_day = getattr(user_data, 'current_day', 1)
            
            if not user_id:
                raise ValueError("User ID not found in user_data")
                
            # Check if we've reached the maximum day
            if current_day > MAX_DAYS:
                await show_block(message, 'FINAL')
                return
                
            # Show the appropriate START block for the current day
            block_name = f'START{current_day}'
            await show_block(message, block_name)
            
            # Update user's last active time in the database
            await db.update_user(
                user_id=user_id,
                last_active=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error in _show_user_day: {str(e)}")
            # Fallback to day 1 if there's an error
            await show_block(message, 'START1')
            
            # If we have a user ID, try to update their day to 1 as a fallback
            if 'user_id' in locals() and user_id:
                try:
                    await db.set_user_day(user_id, 1)
                except Exception as update_error:
                    logger.error(f"Failed to reset user day to 1: {str(update_error)}")
    
    async def _show_block(self, message: Message, block_name: str, user_data = None) -> None:
        """Show a specific block with proper formatting."""
        from ui_blocks import show_block
        
        await show_block(
            message=message,
            block_name=block_name,
            user_data=user_data,
            final_callback=self._handle_final_block,
            start_callback=self._handle_start_block
        )
    
    async def handle_daily(self, message: Message) -> None:
        """Handle /daily command - show daily tasks and progress."""
        user = message.from_user
        user_data = await self.db.get_user(user.id)
        
        if not user_data:
            await message.answer("Пожалуйста, начните с команды /start")
            return
            
        await message.answer(
            "📅 Ваш дневной прогресс:",
            reply_markup=build_marathon_progress(user_data)
        )
    
    async def handle_profile(self, message: Message) -> None:
        """Handle /profile command - show user profile."""
        user = message.from_user
        user_data = await self.db.get_user(user.id)
        
        if not user_data:
            await message.answer("Пожалуйста, начните с команды /start")
            return
            
        await message.answer(
            "👤 Ваш профиль:",
            reply_markup=build_profile_menu(user_data)
        )
    
    async def handle_help(self, message: Message) -> None:
        """Handle /help command - show help information."""
        await message.answer(
            "❓ Помощь и поддержка:",
            reply_markup=build_help_menu()
        )
    
    async def handle_settings(self, message: Message) -> None:
        """Handle /settings command - show settings menu."""
        user = message.from_user
        user_data = await self.db.get_user(user.id)
        
        if not user_data:
            await message.answer("Пожалуйста, начните с команды /start")
            return
            
        await message.answer(
            "⚙️ Настройки:",
            reply_markup=build_settings_menu(user_data)
        )
    
    async def handle_referral(self, message: Message) -> None:
        """Handle /referral command - show referral information."""
        user = message.from_user
        user_data = await self.db.get_user(user.id)
        
        if not user_data:
            await message.answer("Пожалуйста, начните с команды /start")
            return
            
        bot_username = (await message.bot.get_me()).username
        referral_link = f"https://t.me/{bot_username}?start=ref{user.id}"
        await message.answer(
            f"🤝 Реферальная программа\n\n"
            f"Ваша реферальная ссылка: {referral_link}\n\n"
            "Приглашайте друзей и получайте бонусы!"
        )
    
    async def handle_admin(self, message: Message) -> None:
        """Handle admin commands."""
        user = message.from_user
        
        # Check if user is admin
        if user.id not in settings.bot.admin_ids:
            await message.answer("У вас нет прав для выполнения этой команды.")
            return
            
        # TODO: Implement admin commands
        await message.answer("🔧 Админ-панель")
    
    # Helper methods
    async def _show_main_menu(self, message: Message, user_data: Dict[str, Any]) -> None:
        """Show main menu to the user."""
        await message.answer(
            "🏠 Главное меню:",
            reply_markup=build_main_menu(user_data)
        )
    
    async def _send_error(self, message: Message, error_msg: str) -> None:
        """Send error message to user."""
        try:
            await message.answer(f"❌ {error_msg}")
        except Exception as e:
            logger.error(f"Error sending error message: {e}")


    # ===== Registration Flow =====
    
    async def handle_nickname_input(self, message: Message, state: FSMContext) -> None:
        """Handle nickname input during registration (JOIN2)."""
        nickname = message.text.strip()
        
        # Validate nickname
        if not 2 <= len(nickname) <= 32:
            await message.answer("Псевдоним должен быть от 2 до 32 символов. Попробуйте ещё раз:")
            return
            
        # Save nickname to database
        await self.db.update_user(message.from_user.id, {'nickname': nickname})
        
        # Show role selection (JOIN3)
        await self._show_block(message, 'JOIN3')
        await state.set_state(RegistrationStates.awaiting_role)
    
    # ===== Main Commands =====
    
    async def handle_status(self, message: Message) -> None:
        """Show user status page."""
        await self._show_block(message, 'LB_STATUS')
    
    async def handle_shop(self, message: Message) -> None:
        """Show in-game shop."""
        await self._show_block(message, 'LB_SHOP')
    
    async def handle_invest(self, message: Message) -> None:
        """Show investment page."""
        await self._show_block(message, 'INVEST')
    
    # ===== Partner Integrations =====
    
    async def handle_donna(self, message: Message) -> None:
        """Handle DONNA AI partner integration."""
        await self._show_block(message, 'LB_DONNA')
    
    async def handle_unilive(self, message: Message) -> None:
        """Handle Unilive partner integration."""
        await self._show_block(message, 'LB_UNI')
    
    async def handle_5life(self, message: Message) -> None:
        """Handle 5Life partner integration."""
        await self._show_block(message, 'LP_5LIFE')
    
    async def handle_axiom(self, message: Message) -> None:
        """Handle Axiom partner integration."""
        await self._show_block(message, 'LP_AXIOM')
    
    # ===== Other Features =====
    
    async def handle_feedback(self, message: Message) -> None:
        """Handle user feedback."""
        await self._show_block(message, 'FEED_RUN')
    
    async def handle_freya(self, message: Message) -> None:
        """Handle Freya AI assistant."""
        await self._show_block(message, 'FREYA_AICON')
    
    # ===== Callback Handlers =====
    
    async def handle_reset_confirm(self, callback_query: CallbackQuery, state: FSMContext) -> None:
        """Handle account reset confirmation."""
        if callback_query.data == 'reset_confirm':
            await self._show_block(callback_query.message, 'RESET_CON')
            # Add reset logic here
        else:
            await self._show_block(callback_query.message, 'LB_STATUS')
    
    async def handle_begin_game(self, callback_query: CallbackQuery) -> None:
        """Handle game start from callback."""
        user_data = await self.db.get_user(callback_query.from_user.id)
        await self._show_user_day(callback_query.message, user_data)
    
    async def handle_life_book(self, callback_query: CallbackQuery) -> None:
        """Show Life Book main menu."""
        await self._show_block(callback_query.message, 'LB_START')
    
    # ===== Helper Methods =====
    
    async def _handle_final_block(self, message: Message, user_data: Dict[str, Any]) -> None:
        """Handle final block logic."""
        # Add any final block specific logic here
        pass
    
    async def _handle_start_block(self, block_name: str, message: Message, user_data: Dict[str, Any]) -> None:
        """Handle start block logic."""
        from aiogram.fsm.context import FSMContext
        from aiogram.fsm.state import State, StatesGroup
        
        # Get FSM context
        fsm_context = FSMContext(
            storage=self.dp.storage,
            key=FSMContext(
                storage=self.dp.storage,
                key=f"fsm:{message.chat.id}:{message.from_user.id}"
            )
        )
        
        try:
            # Get or create user in database
            user = await self.db.get_or_create_user(
                user_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
            
            # Convert user to dict if it's an object
            if hasattr(user, 'model_dump'):
                user_dict = user.model_dump()
            elif hasattr(user, '__dict__'):
                user_dict = vars(user)
            else:
                user_dict = user if isinstance(user, dict) else {}
            
            # If user doesn't have a nickname, ask for one
            if not user_dict.get('nickname'):
                class RegistrationStates(StatesGroup):
                    awaiting_nickname = State()
                
                await message.answer("👤 Пожалуйста, введите ваш псевдоним (от 3 до 32 символов):")
                await fsm_context.set_state(RegistrationStates.awaiting_nickname)
                return
                
        except Exception as e:
            print(f"Error in _handle_start_block: {str(e)}")
            # Continue with the block even if there's an error with nickname handling
        
        # Clear any existing state
        try:
            await fsm_context.clear()
        except Exception as e:
            print(f"Error clearing state: {str(e)}")
        
        # Show main menu
        await self._show_main_menu(message, user)
    
    async def process_callback(self, callback_query: CallbackQuery) -> None:
        """Process callback queries from inline buttons."""
        await callback_query.answer()  # Acknowledge the callback
        data = callback_query.data
        
        # Example of processing callback data
        if data.startswith('menu_'):
            action = data.split('_', 1)[1]
            if action == 'profile':
                await self.handle_profile(callback_query.message)
            elif action == 'settings':
                await self.handle_settings(callback_query.message)
            # Add more menu actions as needed


def setup_handlers(dp: Router, db: DatabaseManager) -> None:
    """Register all command and callback handlers."""
    command_handlers = CommandHandlers(db)
    dp.include_router(router)
    logger.info("Command handlers registered")


# Initialize command handlers with database connection
async def init_command_handlers():
    """Initialize command handlers with database connection."""
    from db_manager import get_db
    try:
        db_instance = await get_db()
        if not db_instance:
            raise RuntimeError("Failed to initialize database connection")
        return CommandHandlers(db_instance)
    except Exception as e:
        logger.error(f"Failed to initialize command handlers: {e}")
        raise
