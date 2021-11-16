from app.configs.database_config import database_config
from app.core.logs.logging import get_logger
from tortoise import Tortoise

logger = get_logger(__name__)
_database_config = database_config()

MODULE = 'app'
MODELS = [
    'app.models.sample',
    'app.models.sample_translation'
]
TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'database': _database_config.name,
                'host': _database_config.host,
                'port': _database_config.port,
                'user': _database_config.user,
                'password': _database_config.password,
                'minsize': _database_config.connection_min_size,
                'maxsize': _database_config.connection_max_size
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


async def init():
    logger.info('Initializing connection to the database...')

    Tortoise.init_models(MODELS, MODULE)

    await Tortoise.init(config=TORTOISE_ORM, modules={MODULE: MODELS})

    logger.info('Database connection is initialized!')


async def close():
    logger.info('Shutting down database connection...')

    await Tortoise.close_connections()

    logger.info('Database connection shutdown completed!')
