import logging
from functools import lru_cache

from fastapi import FastAPI
from pydantic.env_settings import BaseSettings
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

logger = logging.getLogger(__name__)


class DatabaseConfig(BaseSettings):
    database: str
    database_host: str
    database_port: str
    database_user: str
    database_password: str
    database_connection_min_size: int = 1
    database_connection_max_size: int = 20

    class Config:
        env_prefix = ''
        env_file = '.env'


@lru_cache
def database_config():
    return DatabaseConfig()


MODULE = 'app'
MODELS = [
    'app.models.sample',
    'app.models.sample_translation'
]
CONFIG = database_config()
TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'database': CONFIG.database,
                'host': CONFIG.database_host,
                'port': CONFIG.database_port,
                'user': CONFIG.database_user,
                'password': CONFIG.database_password,
                'minsize': CONFIG.database_connection_min_size,
                'maxsize': CONFIG.database_connection_max_size
            }
        }
    },
    'apps': {
        MODULE: {
            'models': [*MODELS, 'aerich.models'],
            'default_connection': 'default',
        }
    }
}


def init(app: FastAPI):
    logger.info('Initializing connection to the database...')

    Tortoise.init_models(MODELS, MODULE)

    register_tortoise(app, modules={MODULE: MODELS}, config=TORTOISE_ORM)

    logger.info('Database connection is initialized!')
