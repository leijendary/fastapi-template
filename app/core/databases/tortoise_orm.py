from app.configs.database_config import database_config
from app.core.logs.logging import get_logger
from tortoise import Tortoise

logger = get_logger(__name__)
_config = database_config()

MODULE = 'app'
MODELS = [
    'app.models.sample',
    'app.models.sample_translation'
]
MODULES = {
    MODULE: MODELS
}
APPS = {
    MODULE: {
        'models': [*MODELS, 'aerich.models'],
        'default_connection': 'default',
    }
}
TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'database': _config.name,
                'host': _config.host,
                'port': _config.port,
                'user': _config.user,
                'password': _config.password,
                'minsize': _config.connection_min_size,
                'maxsize': _config.connection_max_size
            }
        }
    },
    'apps': APPS
}


async def init():
    logger.info('Initializing connection to the database...')

    Tortoise.init_models(MODELS, MODULE)

    await Tortoise.init(config=TORTOISE_ORM, modules=MODULES)

    logger.info('Database connection is initialized!')


async def close():
    logger.info('Shutting down database connection...')

    await Tortoise.close_connections()

    logger.info('Database connection shutdown completed!')
