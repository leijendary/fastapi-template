from functools import lru_cache
from logging import (CRITICAL, DEBUG, ERROR, INFO, WARNING, Formatter,
                     StreamHandler, getLogger)

from pydantic import BaseSettings

NAME_MAX_LENGTH = 25


class LoggingConfig(BaseSettings):
    log_level = INFO

    class Config:
        env_prefix = ''
        env_file = '.env'


class ColoredFormatter(Formatter):
    grey = '\x1b[38;21m'
    green = '\x1b[32m'
    yellow = '\x1b[33;21m'
    red = '\x1b[31;21m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    level_name = '%(levelname)s:\t  '
    untabbed_level_name = '%(levelname)s: '
    format = '%(asctime)s: %(name)s:\t%(message)s'

    FORMATS = {
        DEBUG: grey + level_name + reset + format,
        INFO: green + level_name + reset + format,
        WARNING: yellow + untabbed_level_name + reset + format,
        ERROR: red + level_name + reset + format,
        CRITICAL: bold_red + untabbed_level_name + reset + format,
    }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno)
        formatter = Formatter(log_format)

        return formatter.format(record)


@lru_cache
def logging_config():
    return LoggingConfig()


def get_logger(name: str):
    config = logging_config()
    log_handler = StreamHandler()
    log_handler.setLevel(config.log_level)
    log_handler.setFormatter(ColoredFormatter())

    name = format_name(name)
    logger = getLogger(name)
    logger.setLevel(config.log_level)
    logger.addHandler(log_handler)

    return logger


def format_name(name: str):
    if len(name) > NAME_MAX_LENGTH and '.' in name:
        splits = name.split('.')

        for i, value in enumerate(splits[:-1]):
            splits[i] = value[:1]

        name = '.'.join(splits)

    return name.ljust(NAME_MAX_LENGTH)[-NAME_MAX_LENGTH:]
