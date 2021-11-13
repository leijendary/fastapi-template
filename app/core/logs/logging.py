from logging import (CRITICAL, DEBUG, ERROR, INFO, WARNING, Formatter,
                     StreamHandler, getLogger)

from app.configs.logging_config import logging_config

config = logging_config()


class ColoredFormatter(Formatter):
    grey = '\x1b[38;21m'
    green = '\x1b[32m'
    yellow = '\x1b[33;21m'
    red = '\x1b[31;21m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    level_name = '%(levelname)s:\t  '
    untabbed_level_name = '%(levelname)s: '
    format = '%(asctime)s: %(name)s: %(message)s'

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


def get_logger(name: str):
    log_handler = StreamHandler()
    log_handler.setLevel(config.level)
    log_handler.setFormatter(ColoredFormatter())

    name = format_name(name)
    logger = getLogger(name)
    logger.setLevel(config.level)
    logger.addHandler(log_handler)

    return logger


def format_name(name: str):
    name_max_length = config.name_max_length

    if len(name) > name_max_length and '.' in name:
        splits = name.split('.')

        for i, value in enumerate(splits[:-1]):
            splits[i] = value[:1]

        name = '.'.join(splits)

    return name.ljust(name_max_length)[-name_max_length:]
