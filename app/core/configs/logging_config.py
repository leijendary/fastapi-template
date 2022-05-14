from functools import lru_cache
from logging import INFO

from pydantic import BaseSettings


class LoggingConfig(BaseSettings):
    level = INFO
    format = "%(asctime)s [%(process)d] [%(levelname)s] %(message)s"
    date_format = "[%Y-%m-%d %H:%M:%S %z]"
    access = False

    class Config:
        env_prefix = "log_"
        env_file = ".env"


@lru_cache
def logging_config() -> LoggingConfig:
    return LoggingConfig()
