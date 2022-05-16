from datetime import datetime, timezone
from logging import LogRecord, Formatter
from logging import StreamHandler, getLogger

from uvicorn.config import LOGGING_CONFIG

from app.core.configs.logging_config import logging_config

_config = logging_config()
_level = _config.level
_format = _config.format
_date_format = _config.date_format
_formatter = Formatter(fmt=_config.format, datefmt=_config.date_format)

# Override uvicorn log format
LOGGING_CONFIG["formatters"]["default"]["fmt"] = _config.format


def get_logger(name: str):
    log_handler = StreamHandler()
    log_handler.setLevel(_config.level)
    log_handler.setFormatter(_formatter)

    logger = getLogger(name)
    logger.setLevel(_config.level)
    logger.addHandler(log_handler)

    return logger


def _format_date(_, record: LogRecord, __):
    return (
        datetime
            .fromtimestamp(record.created, timezone.utc)
            .strftime(_config.date_format)
    )


# Override time formatter
Formatter.formatTime = _format_date