from app.core.configs.database_config import (primary_database_config,
                                              readonly_database_config)
from app.core.logs.logging import get_logger
from app.core.models import signal
from tortoise import Tortoise

logger = get_logger(__name__)
_primary_config = primary_database_config()
_readonly_config = readonly_database_config()

MODULE = "app"
MODELS = [
    "app.models.sample",
    "app.models.sample_translation",
]
MODULES = {
    MODULE: MODELS
}
APPS = {
    MODULE: {
        "models": [*MODELS, "aerich.models"],
        "default_connection": "primary",
    }
}
TORTOISE_ORM = {
    "connections": {
        "primary": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": _primary_config.name,
                "host": _primary_config.host,
                "port": _primary_config.port,
                "user": _primary_config.user,
                "password": _primary_config.password,
                "minsize": _primary_config.connection_min_size,
                "maxsize": _primary_config.connection_max_size
            }
        },
        "readonly": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": _readonly_config.name,
                "host": _readonly_config.host,
                "port": _readonly_config.port,
                "user": _readonly_config.user,
                "password": _readonly_config.password,
                "minsize": _readonly_config.connection_min_size,
                "maxsize": _readonly_config.connection_max_size
            }
        }
    },
    "apps": APPS,
    "routers": ["app.core.models.model.Router"]
}


async def init():
    logger.info("Initializing connection to the database...")

    Tortoise.init_models(MODELS, MODULE)

    await Tortoise.init(config=TORTOISE_ORM, modules=MODULES)

    signal.init()

    logger.info("Database connection is initialized!")


async def close():
    logger.info("Shutting down database connection...")

    await Tortoise.close_connections()

    logger.info("Database connection shutdown completed!")


async def health():
    try:
        result = await Tortoise \
            .get_connection(next(iter(Tortoise._connections))) \
            .execute_query_dict("SELECT 'UP' as status")

        return result[0]["status"] or "DOWN"
    except:
        return "DOWN"
