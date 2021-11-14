from functools import lru_cache

from pydantic.env_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    name: str
    host: str
    port: str
    user: str
    password: str
    connection_min_size: int = 10
    connection_max_size: int = 20

    class Config:
        env_prefix = 'database_'
        env_file = '.env'


@lru_cache
def database_config():
    return DatabaseConfig()
