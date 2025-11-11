# Life-Book Refactoring Plan (Migrating to aiogram 3.x)

## 1. Project Structure

### Core Application
- `lifebook.py` - Main application entry point
- `logger.py` - Centralized logging system
- `config.py` - Application configuration
- `const.py` - Constants and enums


### Business Logic
- `logical_new.py` - New logic implementations
- `marathon_logic.py` - Marathon core logic
- `referral_logic.py` - Referral system
- `ai_manager.py` - AI integration
- `report_manager.py` - Reporting functionality
- `command_handlers.py` - Main command handlers
- `moderator.py` - Moderator commands
- `media_handler.py` - Media processing



### Database
- `lifeman.py` - Core Database driver
- `db_manager.py` - Database operations
- `db_schema.py` - Database schema definitions


### Time m
- `cron_manager.py` - Scheduled tasks
- `ambacron.py` - Cron job management
- `temporal.py` - Time-related functions


### UI Components
- `ui_blocks.py` - UI elements and templates


### Utilities
- `utils.py` - Utility functions
- `lifeBlock.py` - Block dictionary
- `answers.py` - Response templates
- `passive.py` - passive lib
- `active.py` - Active lib

### AI module
- `free11ray.py` - ai core
- `freya.ini` - Freya configuration
- `fre0lib.py` - Core library functions
- `fre0gen.py` - Generation utilities

### Configuration & Scripts
- `go.cmd` - Launch script
- `ewa.cmd` - Development script
- `.env` - Environment variables
- `requirements.txt` - Python dependencies

### Documentation
- `readme.md` - Project documentation
- `taks.md` - Task list
- `Dewiar_FREYA.md` - Freya documentation
- `refactoring_plan.md` - This file


план рефактооринга


1. собрать бот на aiogram 3.x
2. ланчер lifebook
3. логика logical_new
4. база данных драйвер lifeman
5. модули ИИ (не трогать!)
- `free11ray.py` - ai core
- `freya.ini` - Freya configuration
- `fre0lib.py` - Core library functions
- `fre0gen.py` - Generation utilities
6. прочие модули
- `marathon_logic.py` - Marathon core logic
- `referral_logic.py` - Referral system
- `ai_manager.py` - AI integration
- `report_manager.py` - Reporting functionality
- `command_handlers.py` - Main command handlers
- `moderator.py` - Moderator commands
- `media_handler.py` - Media processing
- `ui_blocks.py` - UI elements and templates
- `utils.py` - Utility functions
- `lifeBlock.py` - Block dictionary
- `answers.py` - Response templates
- `passive.py` - passive lib
- `active.py` - Active lib
- `db_manager.py` - Database operations
- `db_schema.py` - Database schema definitions
- `cron_manager.py` - Scheduled tasks
- `ambacron.py` - Cron job management
- `temporal.py` - Time-related functions

8. убедиться что везде применен aiogram
9. проверить логику бота от начала до конца, проверить наличие дублирований
10. модули которые не нужны (разобрать, убрать код в новые модули)
- `passive.py` - passive lib
- `active.py` - Active lib
- `ambacron.py` - Cron job management
- `report_manager.py` - Reporting functionality
- `moderator.py` - Moderator commands



Продолжение - задача для HIVE AI

1. если новый юзер - идет регистрация черезз блоки JOIN1 JOIN2 JOIN3 JOIN4
если старый юззер идет старт START1 START2  итд

чтобы это понять изучи логику файла logical_old.py  - он не используется в боте, это старая версия.
на ее основе этой логики должен работать logical_new.py и вызывать текстоблоки из словаря lifeBlock.py,
изучи его, там все блоки настроены, надо подогнать движок на основе старой модели. Убираешь дубли если есть


2. логер везде оптимизировать, если принты не убирать - дублировать в лог, на экран консоли миниальный вывод
3. ВЫВОД - используй UI модуль, текстоблоки для логики и SEX, SEFOB итд для прочих блоков, также используй все что есть в либах!
4. версия бота aiogram, если найдешь старый формат telegram api update/context то заменяй на новый aiogram.

5. проверь все модули "*.py"
на предмет ошибок в плане рефакторинга

6. AI module не менять логику, там все работает

7. .env проверить, оставить только секретные токены согласно списку, все прочее вынести в конфиг, убрать ненужное
LB_BOT__TOKEN_TEST=7345279574:xxx
LB_BOT__TOKEN_SERVER=7102218284:xxx
LB_BOT__URL_TEST=https://t.me/Lifetestbook_bot
LB_BOT__URL_SERVER=https://t.me/Book_of_lifebot
LB_BOT__WEBHOOK_URL=https://your-domain.com/webhook


8. переделка полная, найти каждый блок в словаре блоков, понять когда он вызывается, прописать

9. все настройки каждого модуля выносим в конфиг , кроме локальных констант, а также в файл констант
10. убираем дубли и мусор

active.py
ai_manager.py
ambacron.py
answers.py
command_handlers.py
config.py
const.py
cron_manager.py
db_manager.py
db_schema.py
fre0gen.py
fre0lib.py
free11ray.py
lifeBlock.py
lifebook.py
lifeman.py
logger.py
logical_new.py
logical_old.py - для анализа только
marathon_logic.py
media_handler.py
moderator.py
passive.py
referral_logic.py
report_manager.py
temporal.py
ui_blocks.py
utils.py

.env - среда (для конфига)
ewa.cmd - кативатор среды
go.cmd - бат ланчер
lifebook.db - текущая база
freya.ini конфиг для ИИ
readme.md описатель проекта
refactoring_plan.md план текущего рефактора
requirements.txt рекваирмент

