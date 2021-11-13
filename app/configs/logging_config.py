from functools import lru_cache
from logging import INFO

from pydantic import BaseSettings


class LoggingConfig(BaseSettings):
    level = INFO
    name_max_length = 20

    class Config:
        env_prefix = 'log_'
        env_file = '.env'


@lru_cache
def logging_config():
    return LoggingConfig()
