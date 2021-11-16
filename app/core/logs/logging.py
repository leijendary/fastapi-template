from logging import (CRITICAL, DEBUG, ERROR, INFO, WARNING, Formatter,
                     StreamHandler, getLogger)

from app.configs.logging_config import logging_config

config = logging_config()


class LogFormatter(Formatter):
    level_name = '%(levelname)s:\t  '
    untabbed_level_name = '%(levelname)s:  '
    format = '%(asctime)s: %(name)s: %(message)s'

    FORMATS = {
        DEBUG: level_name + format,
        INFO: level_name + format,
        WARNING: untabbed_level_name + format,
        ERROR: level_name + format,
        CRITICAL: untabbed_level_name + format,
    }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno)
        formatter = Formatter(log_format)

        return formatter.format(record)


def get_logger(name: str):
    log_handler = StreamHandler()
    log_handler.setLevel(config.level)
    log_handler.setFormatter(LogFormatter())

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
