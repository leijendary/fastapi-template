import subprocess
from datetime import datetime

import uvicorn
from botocore.exceptions import ClientError
from elasticsearch.exceptions import NotFoundError as SearchNotFoundError
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_pagination import add_pagination
from jose.exceptions import ExpiredSignatureError
from pydantic.error_wrappers import ValidationError
from pydantic.json import ENCODERS_BY_TYPE
from starlette.middleware import Middleware
from tortoise.exceptions import IntegrityError

from app.api.v1.routers import sample_router as sample_router_v1
from app.configs.app_config import app_config
from app.configs.logging_config import logging_config
from app.configs.security_config import security_config
from app.core.cache import redis_cache
from app.core.clients import httpx_client
from app.core.data.data_response import DataResponse
from app.core.data.error_response import ErrorResponse
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
from app.core.search import elasticsearch
from app.core.utils.date_util import to_epoch
from app.events import consumers

# Override datetime encoder for the json response
ENCODERS_BY_TYPE[datetime] = to_epoch

_config = app_config()

# Possible responses
responses = {
    200: {
        'description': 'Success',
        'model': DataResponse
    },
    201: {
        'description': 'Resource created',
        'model': DataResponse
    },
    400: {
        'description': 'Unauthorized',
        'model': ErrorResponse
    },
    403: {
        'description': 'Access Denied',
        'model': ErrorResponse
    },
    404: {
        'description': 'Resource not found',
        'model': ErrorResponse
    },
    405: {
        'description': 'Method not allowed',
        'model': ErrorResponse
    },
    409: {
        'description': 'Unique constraint error',
        'model': ErrorResponse
    },
    422: {
        'description': 'Validation error',
        'model': ErrorResponse
    },
    500: {
        'description': 'Internal server error',
        'model': ErrorResponse
    }
}

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
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    ),
    Middleware(GZipMiddleware),
]

# Routers
routers = [
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
        title='FastAPI Template',
        version='0.0.1',
        responses=responses,
        exception_handlers=exception_handlers,
        middleware=middleware,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )

    # Include all routers
    for router in routers:
        app.include_router(router, prefix=_config.prefix)

    # FastAPI pagination
    add_pagination(app)

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
        ssl_keyfile=security.ssl_keyfile
    )
