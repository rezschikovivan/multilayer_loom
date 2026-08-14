import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = "loom_logs.log"
MAX_BYTES = 3 * 1024 * 1024 # Максимальный размер (3 МБ)
BACKUP_COUNT = 3


def get_logger(name: str) -> logging.Logger:
    file_handler = RotatingFileHandler(
            filename=LOG_FILE,
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT,
            encoding="utf-8"
        )
    file_handler.setLevel(logging.DEBUG)

    log_format = "%(asctime)s - %(levelname)s - [%(name)s] - %(filename)s.%(funcName)s: '%(message)s'"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # В консоль пишем от INFO и выше
    console_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
