import logging
from functools import lru_cache

from pydantic import BaseSettings


class LoggingConfig(BaseSettings):
    log_level = logging.INFO

    class Config:
        env_prefix = ''
        env_file = '.env'


@lru_cache
def logging_config():
    return LoggingConfig()


def get_logger(name: str):
    config = logging_config()
    logging.basicConfig(
        format='%(levelname)s: %(asctime)s: %(name)s:\t%(message)s',
        level=config.log_level
    )
    logger = logging.getLogger(name)

    return logger
