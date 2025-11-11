"""
Centralized logging configuration for the application.
All modules should import the logger from this module.

Usage:
    from logger import logger
    logger.info("Message")  # Goes to file and minimal console
    logger.debug("Debug message")  # Goes to file only (unless debug mode)
"""
import sys
import logging
from pathlib import Path
from typing import Optional

from config import config, logging_config

# Создаем корневой логгер
logger = logging.getLogger()
logger.setLevel(logging.DEBUG if config.debug else getattr(logging, logging_config.level))

# Формат логов для файла (подробный)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Формат логов для консоли (минимальный)
console_formatter = logging.Formatter(
    "%(levelname)s - %(message)s"
)

class NoisyFilter(logging.Filter):
    """Фильтр для исключения 'is not handled' сообщений."""
    def filter(self, record):
        return "is not handled" not in record.getMessage()

class MinimalConsoleFilter(logging.Filter):
    """Фильтр для минимального вывода в консоль (только WARNING и выше)."""
    def filter(self, record):
        # В минимальном режиме показываем только WARNING и выше
        if logging_config.get('console_minimal', True):
            return record.levelno >= logging.WARNING
        return True

def setup_logging(log_file: Optional[str] = None) -> None:
    """
    Настройка системы логирования.

    Логирование настроено следующим образом:
    - Файл: полный лог всех сообщений с подробным форматированием
    - Консоль: минимальный вывод (только WARNING и выше), если включен console_minimal
    - Print statements не дублируются в лог автоматически - используйте logger

    Args:
        log_file: Путь к файлу лога. Если None, используется значение из конфига.
    """
    global logger

    # Создаем директорию для логов, если её нет
    log_dir = Path(logging_config.get('logs_dir', 'logs'))
    log_dir.mkdir(exist_ok=True)

    # Если файл не указан, используем значение из конфига
    if log_file is None:
        log_file = log_dir / logging_config.get('file', 'lifebook.log')

    # Обработчик для консоли (с минимальным выводом)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(NoisyFilter())
    console_handler.addFilter(MinimalConsoleFilter())  # Минимальный вывод

    # Обработчик для файла (полный лог)
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
        mode="a"
    )
    file_handler.setFormatter(file_formatter)  # Подробный формат для файла
    file_handler.addFilter(NoisyFilter())

    # Удаляем все существующие обработчики
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Добавляем наши обработчики
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Note: We do NOT redirect stdout/stderr to avoid duplicating print statements
    # According to issue requirements: "prints should not be duplicated in log"
    # Developers should use logger.info() instead of print() for logging

    logger.info("Logging initialized - minimal console output mode enabled")

# Инициализируем логирование при импорте модуля
setup_logging()
