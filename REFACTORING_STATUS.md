# Life-Book Refactoring Status

## Overview
This document tracks the progress of refactoring the Life-Book bot from the old Telegram API to aiogram 3.x, as outlined in issue #1.

## Completed Tasks ✅

### 1. Configuration Refactoring (Points 7, 9)
- **Status**: ✅ COMPLETED
- **Files Modified**: `.env`, `config.py`
- **Changes**:
  - Refactored `.env` to contain only secret tokens (bot tokens, API keys, secrets)
  - Moved all non-secret settings to `config.py`
  - Added comprehensive config sections: paths, marathon, logging, external services
  - Added convenience accessors for all config sections

### 2. Logger Optimization (Point 2)
- **Status**: ✅ COMPLETED
- **Files Modified**: `logger.py`
- **Changes**:
  - Implemented minimal console output (only WARNING+ messages)
  - Full detailed logs still go to file
  - Removed stdout/stderr redirection to avoid print duplication
  - Added comprehensive documentation

### 3. Code Analysis
- **Status**: ✅ COMPLETED
- **Analysis Results**:
  - Identified 14 modules using old Telegram API (telegram, telegram.ext)
  - Documented the flow logic from `logical_old.py`
  - Understood the block system in `lifeBlock.py`
  - Analyzed current `logical_new.py` implementation

## In Progress Tasks 🔄

### 4. logical_new.py Implementation (Points 1, 3, 8)
- **Status**: 🔄 IN PROGRESS
- **Requirements**:
  - Implement complete flow from `logical_old.py`
  - New users: JOIN1 → JOIN2 → JOIN3 → JOIN4 → registration
  - Existing users: START1 → START2 → main menu
  - Use text blocks from `lifeBlock.py` via `ui_blocks.py`
  - Remove duplicates from old implementation

**Key Functions to Port**:
```python
# From logical_old.py:
- START_AGAIN() - restart flow
- START_JOIN() - new user registration (JOIN1-4)
- START_LIFE() - existing user flow (START1-2)
- START_PRO() - professional/premium flow
- START_BOOK() - book/marathon flow
- START_DAY() - daily task flow
- BUTTON_RUN() - callback handler
- INPUT_RUN() - text input handler
```

## Pending Tasks 📋

### 5. Replace Old Telegram API (Point 4)
- **Status**: 📋 PENDING
- **Affected Files** (14 modules):
  ```
  passive.py
  report_manager.py
  temporal.py
  ui_blocks.py
  utils.py
  moderator.py
  fre0lib.py
  free11ray.py
  cron_manager.py
  fre0gen.py
  active.py
  ai_manager.py
  ambacron.py
  ```

**Migration Pattern**:
```python
# OLD (telegram):
from telegram import Update
from telegram.ext import ContextTypes

# NEW (aiogram 3.x):
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
```

### 6. Remove Duplicates and Cleanup (Point 10)
- **Status**: 📋 PENDING
- **Candidates for Removal/Consolidation**:
  - `passive.py` - passive lib (analyze and integrate)
  - `active.py` - active lib (analyze and integrate)
  - `ambacron.py` - cron job management (consolidate with cron_manager.py)
  - `report_manager.py` - reporting (analyze usage)
  - `moderator.py` - moderator commands (check if still needed)

### 7. Verify AI Module (Point 6)
- **Status**: ⚠️ DO NOT CHANGE
- **Modules**: `free11ray.py`, `fre0lib.py`, `fre0gen.py`, `freya.ini`
- **Note**: These work correctly, only update API calls if needed

## Technical Debt & Notes

### Block System Implementation
The `lifeBlock.py` defines all text blocks used in the bot:
- JOIN1-4: New user registration blocks
- START1-2: Existing user start blocks
- LB_STATUS: User status page
- LB_DAILY: Daily tasks
- REFER/REFER_FULL: Referral system
- And many more...

All blocks should be accessed via `ui_blocks.py` helper functions:
```python
from ui_blocks import send_block, get_life_block, format_block_text
```

### State Management
Old code used `context.user_data` for state. New code should use:
```python
from aiogram.fsm.context import FSMContext
# States defined in separate file or class
```

### Database Integration
Current implementation uses:
- `lifeman.py` - core database driver
- `db_manager.py` - database operations
- `db_schema.py` - schema definitions

Ensure all new code uses async database operations.

## Recommendations for Next Steps

1. **Priority 1**: Complete `logical_new.py` implementation
   - Port all essential flows from `logical_old.py`
   - Ensure JOIN1-4 and START1-2 flows work
   - Test registration and login

2. **Priority 2**: Update critical modules to aiogram 3.x
   - Start with `ui_blocks.py` (used by logical_new.py)
   - Then `utils.py` (shared utilities)
   - Then command handlers

3. **Priority 3**: Remove duplicates
   - Analyze passive.py and active.py usage
   - Consolidate cron modules
   - Remove unnecessary modules

4. **Priority 4**: Testing
   - Test new user registration flow
   - Test existing user login flow
   - Test daily tasks flow
   - Test referral system

## Module Dependencies Map

```
lifebook.py (main entry)
├── config.py ✅
├── logger.py ✅
├── logical_new.py 🔄 (needs complete implementation)
│   ├── ui_blocks.py ⚠️ (uses old API)
│   ├── db_manager.py
│   └── const.py
├── command_handlers.py ⚠️
├── cron_manager.py ⚠️
└── utils.py ⚠️
```

Legend:
- ✅ = Refactored
- 🔄 = In progress
- ⚠️ = Needs aiogram 3.x update
- ❌ = Old version (logical_old.py)

## Testing Checklist

- [ ] New user can register (JOIN1-4 flow)
- [ ] Existing user can login (START1-2 flow)
- [ ] User can access daily tasks
- [ ] User can fill diary entries
- [ ] Referral system works
- [ ] Cron jobs trigger correctly
- [ ] Logger outputs correctly (minimal console, full file)
- [ ] No old telegram API imports remain in active code

## Files Modified

1. `.env` - Refactored to secrets only
2. `config.py` - Added all non-secret settings
3. `logger.py` - Optimized for minimal console output

## Files to Create/Update

1. `logical_new.py` - Complete implementation (in progress)
2. `ui_blocks.py` - Update to aiogram 3.x
3. `utils.py` - Update to aiogram 3.x
4. `command_handlers.py` - Update to aiogram 3.x

## Estimated Effort Remaining

- Complete logical_new.py: 4-6 hours
- Update 14 modules to aiogram 3.x: 8-12 hours
- Testing and bug fixes: 4-6 hours
- **Total**: 16-24 hours

---
Last Updated: 2025-11-11
