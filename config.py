"""
Simplified configuration management for Life-Book bot.

This module provides a simple configuration system that loads settings from:
1. Environment variables (highest priority)
2. .env file in the project root (loaded by python-dotenv)
3. Default values (lowest priority)
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Environment types
class Environment:
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Config:
    """Simple configuration class that mimics a dict but allows dot notation."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.__dict__[key] = Config(**value)
            else:
                self.__dict__[key] = value
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def get(self, key, default=None):
        return self.__dict__.get(key, default)
    
    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Config):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result

# Default configuration
DEFAULT_CONFIG = {
    "debug": os.getenv("LB_DEBUG", "false").lower() == "true",
    "log_level": os.getenv("LB_LOG_LEVEL", "INFO"),
    "admins": {
        "moderators": [456781641, 6794691889],  # Bogdan, John
        "admins": [6794691889, 456781641, 458972922],  # John, Bogdan, Olesa
        "revisors": [1802577464, 458972922]  # Gena, Gorin
    },
    "chats": {
        "life_chat_id": -1002232747079,
        "pay_chat_id": -1002562493765,
        "dev_chat_id": -1002232747079  # Same as life_chat_id
    },
    "secret_key": os.getenv("LB_SECRET_KEY", "change-me-in-production"),
    
    "bot": {
        "token_test": os.getenv("LB_BOT__TOKEN_TEST", ""),
        "token_server": os.getenv("LB_BOT__TOKEN_SERVER", ""),
        "url_test": os.getenv("LB_BOT__URL_TEST", "https://t.me/test_bot"),
        "url_server": os.getenv("LB_BOT__URL_SERVER", "https://t.me/prod_bot"),
        "admin_ids": [int(x.strip("[] ")) for x in os.getenv("LB_BOT__ADMIN_IDS", "[]").split(",") if x.strip("[] ")],
        "moderator_ids": [int(x.strip("[] ")) for x in os.getenv("LB_BOT__MODERATOR_IDS", "[]").split(",") if x.strip("[] ")],
        "revisor_ids": [int(x.strip("[] ")) for x in os.getenv("LB_BOT__REVISOR_IDS", "[]").split(",") if x.strip("[] ")],
        "use_webhook": os.getenv("LB_BOT__USE_WEBHOOK", "false").lower() == "true",
        "webhook_url": os.getenv("LB_BOT__WEBHOOK_URL"),
        "webhook_port": int(os.getenv("LB_BOT__WEBHOOK_PORT", "8443")),
        "rate_limit": int(os.getenv("LB_BOT__RATE_LIMIT", "30")),
    },
    
    "database": {
        "url": os.getenv("LB_DATABASE_URL", "sqlite+aiosqlite:///./lifebook.db"),
        "echo": os.getenv("LB_DATABASE_ECHO", "false").lower() == "true",
        "pool_size": int(os.getenv("LB_DATABASE_POOL_SIZE", "5")),
        "max_overflow": int(os.getenv("LB_DATABASE_MAX_OVERFLOW", "10")),
        "pool_recycle": int(os.getenv("LB_DATABASE_POOL_RECYCLE", "3600")),
    },
    
    "ai": {
        "enabled": os.getenv("LB_AI_ENABLED", "true").lower() == "true",
        "provider": os.getenv("LB_AI_PROVIDER", "openai"),
        "api_key": os.getenv("LB_AI_API_KEY"),
        "model": os.getenv("LB_AI_MODEL", "gpt-3.5-turbo"),
    },
    
    "notifications": {
        "morning_time": os.getenv("LB_NOTIFICATIONS_MORNING_TIME", "09:00"),
        "evening_time": os.getenv("LB_NOTIFICATIONS_EVENING_TIME", "21:00"),
        "timezone": os.getenv("LB_NOTIFICATIONS_TIMEZONE", "Europe/Moscow"),
        "enabled": os.getenv("LB_NOTIFICATIONS_ENABLED", "true").lower() == "true",
    },
}

# Create config instance
config = Config(**DEFAULT_CONFIG)

# Backward compatibility
bot_config = config.bot
db_config = config.database
ai_config = config.ai
notif_config = config.notifications

def get_bot_token() -> str:
    """Get the appropriate bot token based on environment."""
    # Check if token is set in environment variables
    token = os.getenv('LB_BOT__TOKEN_TEST')
    if token:
        return token
        
    # Fallback to config
    env = os.getenv('LB_ENV', 'development')
    return config.bot.token_server if env == 'production' else config.bot.token_test

def get_bot_url() -> str:
    """Get the appropriate bot URL based on environment."""
    env = os.getenv('LB_ENV', 'development')
    return config.bot.url_server if env == 'production' else config.bot.url_test

# Configuration is now initialized directly in the module level
# No need for separate initialization
