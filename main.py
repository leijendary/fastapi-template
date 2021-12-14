import subprocess
from datetime import datetime

import uvicorn
from botocore.exceptions import ClientError
from elasticsearch.exceptions import NotFoundError as SearchNotFoundError
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from jose.exceptions import ExpiredSignatureError
from pydantic.error_wrappers import ValidationError
from pydantic.json import ENCODERS_BY_TYPE
from starlette.middleware import Middleware
from starlette_context.middleware.raw_middleware import RawContextMiddleware
from tortoise.exceptions import IntegrityError

from app.api.v1.routers import sample_router as sample_router_v1
from app.configs.app_config import app_config
from app.configs.logging_config import logging_config
from app.configs.security_config import security_config
from app.core.cache import redis_cache
from app.core.clients import httpx_client
from app.core.data.data_response import DataResponse
from app.core.databases import tortoise_orm
from app.core.errors.access_denied_error import access_denied_handler
from app.core.errors.client_error import client_error_handler
from app.core.errors.expired_token_error import expired_token_handler
from app.core.errors.generic_error import generic_handler
from app.core.errors.integrity_error import integrity_handler
from app.core.errors.invalid_token_error import invalid_token_handler
from app.core.errors.method_not_allowed_error import method_not_allowed_handler
from app.core.errors.not_found_error import not_found_handler
from app.core.errors.resource_not_found_error import resource_not_found_handler
from app.core.errors.search_not_found_error import search_not_found_handler
from app.core.errors.unauthorized_error import unauthorized_handler
from app.core.errors.validation_error import validation_handler
from app.core.events import kafka_producer
from app.core.exceptions.access_denied_exception import AccessDeniedException
from app.core.exceptions.invalid_token_exception import InvalidTokenException
from app.core.exceptions.resource_not_found_exception import \
    ResourceNotFoundException
from app.core.exceptions.unauthorized_exception import UnauthorizedException
from app.core.plugins.request_plugin import AuthorizationPlugin
from app.core.routers import healthcheck_router
from app.core.search import elasticsearch
from app.core.utils.date_util import to_epoch
from app.events import consumers

# Override datetime encoder for the json response
ENCODERS_BY_TYPE[datetime] = to_epoch

_config = app_config()

# Global exception handlers
exception_handlers = {
    404: not_found_handler,
    405: method_not_allowed_handler,
    InvalidTokenException: invalid_token_handler,
    UnauthorizedException: unauthorized_handler,
    ExpiredSignatureError: expired_token_handler,
    AccessDeniedException: access_denied_handler,
    ResourceNotFoundException: resource_not_found_handler,
    SearchNotFoundError: search_not_found_handler,
    IntegrityError: integrity_handler,
    RequestValidationError: validation_handler,
    ValidationError: validation_handler,
    ClientError: client_error_handler,
    Exception: generic_handler
}

# Middlewares
middleware = [
    Middleware(RawContextMiddleware, plugins=[AuthorizationPlugin()])
]

# Routers
routers = [
    healthcheck_router.router,
    sample_router_v1.router
]

# Startup event
on_startup = [
    tortoise_orm.init,
    elasticsearch.init,
    kafka_producer.init,
    httpx_client.init,
    redis_cache.init,
    consumers.init
]

# Shutdown event
on_shutdown = [
    tortoise_orm.close,
    elasticsearch.close,
    kafka_producer.close,
    httpx_client.close,
    redis_cache.close
]


def create_app() -> FastAPI:
    # App instance
    app = FastAPI(
        title=_config.name,
        version=_config.version,
        default_response_class=DataResponse,
        exception_handlers=exception_handlers,
        middleware=middleware,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )

    # Include all routers
    for router in routers:
        app.include_router(router, prefix=_config.prefix)

    return app


# Create an instance of the app
app = create_app()


def run_prestart():
    # Run prestart shell script
    subprocess.call(['sh', './prestart.sh'])


if __name__ == '__main__':
    security = security_config()
    log = logging_config()
    reload = _config.environment == 'local'

    # Run prestart
    run_prestart()

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=_config.port,
        reload=reload,
        access_log=log.access,
        use_colors=False,
        ssl_certfile=security.ssl_certfile,
        ssl_keyfile=security.ssl_keyfile,
        server_header=False
    )
