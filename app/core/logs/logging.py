from datetime import datetime, timezone
from logging import Formatter, StreamHandler, getLogger

from app.configs.logging_config import logging_config
from uvicorn.config import LOGGING_CONFIG

_logging_config = logging_config()

# Override time formatter
Formatter.formatTime = (lambda self, record, datefmt=None: format_date(record))

# Override uvicorn log format
LOGGING_CONFIG["formatters"]["default"]["fmt"] = _logging_config.format


class LogFormatter(Formatter):

    def format(self, record):
        log_format = _logging_config.format
        formatter = Formatter(log_format)
        formatter.datefmt = _logging_config.date_format

        return formatter.format(record)


def get_logger(name: str):
    log_handler = StreamHandler()
    log_handler.setLevel(_logging_config.level)
    log_handler.setFormatter(LogFormatter())

    logger = getLogger(name)
    logger.setLevel(_logging_config.level)
    logger.addHandler(log_handler)

    return logger


def format_date(record):
    return datetime \
        .fromtimestamp(record.created, timezone.utc) \
        .strftime(_logging_config.date_format)
