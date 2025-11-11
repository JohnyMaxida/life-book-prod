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
    "debug": os.getenv("LB_APP__DEBUG", "false").lower() == "true",
    "demo_mode": os.getenv("LB_APP__DEMO_MODE", "false").lower() == "true",
    "environment": os.getenv("LB_APP__ENVIRONMENT", "development"),
    "version": os.getenv("LB_APP__VERSION", "beta 2"),
    "timezone": os.getenv("LB_APP__TIMEZONE", "Europe/Moscow"),

    "admins": {
        "moderators": [456781641, 6794691889],  # Bogdan, John
        "admins": [6794691889, 456781641, 458972922],  # John, Bogdan, Olesa
        "revisors": [1802577464, 458972922]  # Gena, Gorin
    },
    "chats": {
        "life_chat_id": -1002232747079,
        "pay_chat_id": -1002562493765,
        "gpg_chat_id": -1001788044296,  # ГЖП группа проекта Жизн
        "dev_chat_id": -1002232747079  # Same as life_chat_id
    },
    "secret_key": os.getenv("LB_SECURITY__SECRET_KEY", "change-me-in-production"),
    "jwt_secret": os.getenv("LB_SECURITY__JWT_SECRET", "another-secure-string"),
    "password_salt_rounds": 10,

    "bot": {
        "token_test": os.getenv("LB_BOT__TOKEN_TEST", ""),
        "token_server": os.getenv("LB_BOT__TOKEN_SERVER", ""),
        "url_test": os.getenv("LB_BOT__URL_TEST", "https://t.me/test_bot"),
        "url_server": os.getenv("LB_BOT__URL_SERVER", "https://t.me/prod_bot"),
        "use_webhook": False,  # Set to True only if needed
        "webhook_url": os.getenv("LB_BOT__WEBHOOK_URL"),
        "webhook_port": 8443,
        "rate_limit": 30,
    },

    "database": {
        "url": "sqlite+aiosqlite:///./lifebook.db",
        "echo": False,
        "pool_size": 5,
        "max_overflow": 10,
        "pool_recycle": 3600,
    },

    "ai": {
        "enabled": True,
        "provider": "openai",
        "api_key": os.getenv("LB_AI__API_KEY"),
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 500,
    },

    "notifications": {
        "morning_time": "09:00",
        "evening_time": "21:00",
        "timezone": "Europe/Moscow",
        "enabled": True,
        "weekly_report_day": 0,  # 0 = Monday, 6 = Sunday
    },

    "paths": {
        "data_dir": "DATA-LIFE",
        "art_dir": "DATA-LIFE/life-art",
        "art_block_dir": "DATA-LIFE/art-block",
        "logs_dir": "logs",
        "life_db_file": "dbook.sql",
    },

    "marathon": {
        "max_days": 28,
        "items_per_page": 4,
        "default_tariff": "FREE",
        "tariffs": ["FREE", "PRO"],
    },

    "logging": {
        "level": "INFO",
        "file": "lifebook.log",
        "max_size": 10485760,  # 10MB
        "backup_count": 5,
        "console_minimal": True,  # Minimal console output as per requirements
    },

    "external": {
        "s3_bucket": os.getenv("LB_EXTERNAL__S3_BUCKET", ""),
        "s3_access_key": os.getenv("LB_EXTERNAL__S3_ACCESS_KEY", ""),
        "s3_secret_key": os.getenv("LB_EXTERNAL__S3_SECRET_KEY", ""),
        "email_provider": os.getenv("LB_EXTERNAL__EMAIL_PROVIDER", ""),
        "email_api_key": os.getenv("LB_EXTERNAL__EMAIL_API_KEY", ""),
    },
}

# Create config instance
config = Config(**DEFAULT_CONFIG)

# Backward compatibility and convenience accessors
bot_config = config.bot
db_config = config.database
ai_config = config.ai
notif_config = config.notifications
paths_config = config.paths
marathon_config = config.marathon
logging_config = config.logging
external_config = config.external
admins_config = config.admins
chats_config = config.chats

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
