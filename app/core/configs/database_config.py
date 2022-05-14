from functools import lru_cache
from typing import Optional

from pydantic.env_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    name: Optional[str]
    host: Optional[str]
    port = 5432
    user: Optional[str]
    password: Optional[str]
    connection_min_size: int = 10
    connection_max_size: int = 20


class PrimaryDatabaseConfig(DatabaseConfig):
    class Config:
        env_prefix = "database_primary_"
        env_file = ".env"


class ReadonlyDatabaseConfig(DatabaseConfig):
    class Config:
        env_prefix = "database_readonly_"
        env_file = ".env"


@lru_cache
def primary_database_config() -> PrimaryDatabaseConfig:
    return PrimaryDatabaseConfig()


@lru_cache
def readonly_database_config() -> ReadonlyDatabaseConfig:
    return ReadonlyDatabaseConfig()
