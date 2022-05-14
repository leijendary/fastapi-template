from typing import List

from aerich import Command
from app.core.configs.database_config import (DatabaseConfig,
                                              primary_database_config,
                                              readonly_database_config)
from app.core.constants import CONNECTION_PRIMARY, CONNECTION_READONLY
from app.core.logs.logging import get_logger
from app.core.models import signal
from tortoise import Tortoise

logger = get_logger(__name__)
_primary_config = primary_database_config()
_readonly_config = readonly_database_config()
_module = "app"


async def init(models: List[str]):
    logger.info("Initializing connection to the database...")

    modules = {_module: models}
    config = create_configuration(models)
    command = Command(tortoise_config=config, app=_module)
    await command.init()
    await command.upgrade()

    Tortoise.init_models(models, _module)

    await Tortoise.init(config=config, modules=modules)

    signal.init()

    logger.info("Database connection is initialized!")


async def close():
    logger.info("Shutting down database connection...")

    await Tortoise.close_connections()

    logger.info("Database connection shutdown completed!")


async def health():
    try:
        result = await (
            Tortoise
            .get_connection(next(iter(Tortoise._connections)))
            .execute_query_dict("SELECT 'UP' as status")
        )

        return result[0]["status"] or "DOWN"
    except:
        return "DOWN"


def create_configuration(models: List[str]):
    apps = {
        _module: {
            "models": [*models, "aerich.models"],
            "default_connection": CONNECTION_PRIMARY,
        }
    }
    configuration = {
        "connections": {
            CONNECTION_PRIMARY: _connection(_primary_config),
            CONNECTION_READONLY: _connection(_readonly_config)
        },
        "apps": apps,
        "routers": ["app.core.models.model.Router"]
    }

    return configuration


def _connection(config: DatabaseConfig):
    return {
        "engine": "tortoise.backends.asyncpg",
        "credentials": {
            "database": config.name,
            "host": config.host,
            "port": config.port,
            "user": config.user,
            "password": config.password,
            "minsize": config.connection_min_size,
            "maxsize": config.connection_max_size
        }
    }
