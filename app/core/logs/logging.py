from logging import basicConfig, getLogger

from app.configs.logging_config import logging_config

_logging_config = logging_config()


def get_logger(name: str):
    basicConfig(
        level=_logging_config.level,
        format='[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %z',
    )

    name = format_name(name)
    logger = getLogger(name)

    return logger


def format_name(name: str):
    name_max_length = _logging_config.name_max_length

    if len(name) > name_max_length and '.' in name:
        splits = name.split('.')

        for i, value in enumerate(splits[:-1]):
            splits[i] = value[:1]

        name = '.'.join(splits)

    return name.ljust(name_max_length)[-name_max_length:]
