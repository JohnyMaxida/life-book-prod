"""
Centralized logging configuration for the application.
All modules should import the logger from this module.
"""
import sys
import logging
from pathlib import Path
from typing import Optional

from config import config

# Создаем корневой логгер
logger = logging.getLogger()
logger.setLevel(logging.DEBUG if config.debug else logging.INFO)

# Формат логов
formatter = logging.Formatter(
    "%(levelname)s - %(message)s"
)

class NoisyFilter(logging.Filter):
    """Фильтр для исключения 'is not handled' сообщений."""
    def filter(self, record):
        return "is not handled" not in record.getMessage()

def setup_logging(log_file: Optional[str] = None) -> None:
    """
    Настройка системы логирования.
    
    Args:
        log_file: Путь к файлу лога. Если None, используется значение из конфига.
    """
    global logger
    
    # Создаем директорию для логов, если её нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Если файл не указан, используем значение из конфига
    if log_file is None:
        log_file = log_dir / "lifebook.log"
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.addFilter(NoisyFilter())
    
    # Обработчик для файла
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
        mode="a"
    )
    file_handler.setFormatter(formatter)
    file_handler.addFilter(NoisyFilter())
    
    # Удаляем все существующие обработчики
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Добавляем наши обработчики
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    class StreamToLogger:
        """Класс для перенаправления stdout/stderr в логгер"""
        def __init__(self, logger, log_level=logging.INFO):
            self.logger = logger
            self.log_level = log_level

        def write(self, buf):
            for line in buf.rstrip().splitlines():
                if line.strip():
                    self.logger.log(self.log_level, line.rstrip())
                    
        def flush(self):
            pass
    
    # Перенаправляем стандартный вывод в логгер
    sys.stdout = StreamToLogger(logging.getLogger('STDOUT'), logging.INFO)
    sys.stderr = StreamToLogger(logging.getLogger('STDERR'), logging.ERROR)
    
    logger.info("Логирование инициализировано")

# Инициализируем логирование при импорте модуля
setup_logging()
