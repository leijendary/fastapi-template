import logging
from functools import lru_cache
from logging import Formatter

from pydantic import BaseSettings


class LoggingConfig(BaseSettings):
    log_level = logging.INFO

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
    format = '%(asctime)s: %(name)s:\t%(message)s'

    FORMATS = {
        logging.DEBUG: grey + level_name + reset + format,
        logging.INFO: green + level_name + reset + format,
        logging.WARNING: yellow + level_name + reset + format,
        logging.ERROR: red + level_name + reset + format,
        logging.CRITICAL: bold_red + level_name + reset + format,
    }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format)

        return formatter.format(record)


@lru_cache
def logging_config():
    return LoggingConfig()


def get_logger(name: str):
    config = logging_config()
    log_handler = logging.StreamHandler()
    log_handler.setLevel(config.log_level)
    log_handler.setFormatter(ColoredFormatter())

    logger = logging.getLogger(name)
    logger.setLevel(config.log_level)
    logger.addHandler(log_handler)

    return logger
