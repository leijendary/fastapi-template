from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_pagination import add_pagination
from pydantic.error_wrappers import ValidationError
from pydantic.json import ENCODERS_BY_TYPE
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.api.v1.routers import sample_router as sample_router_v1
from app.configs.app_config import app_config
from app.core.cache import redis_cache
from app.core.clients import httpx_client
from app.core.data.data_response import DataResponse
from app.core.data.error_response import ErrorResponse
from app.core.databases import tortoise_orm
from app.core.errors.generic_error import generic_handler
from app.core.errors.integrity_error import integrity_handler
from app.core.errors.invalid_token import invalid_token_handler
from app.core.errors.not_exists_error import not_exists_handler
from app.core.errors.not_found_error import not_found_handler
from app.core.errors.validation_error import validation_handler
from app.core.events import kafka_consumer
from app.core.exceptions.invalid_token_exception import InvalidTokenException
from app.core.search import elasticsearch
from app.utils.date_util import to_epoch

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
        'description': 'Resource not found',
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
    InvalidTokenException: invalid_token_handler,
    DoesNotExist: not_exists_handler,
    IntegrityError: integrity_handler,
    RequestValidationError: validation_handler,
    ValidationError: validation_handler,
    Exception: generic_handler
}

# Startup event
on_startup = [
    tortoise_orm.init,
    kafka_consumer.init,
    elasticsearch.init,
    redis_cache.init
]

# Shutdown event
on_shutdown = [
    tortoise_orm.close,
    elasticsearch.close,
    httpx_client.close,
    redis_cache.close
]

# App instance
app = FastAPI(
    title='FastAPI Template',
    version='0.0.1',
    responses=responses,
    exception_handlers=exception_handlers,
    on_startup=on_startup,
    on_shutdown=on_shutdown
)

# Routers
app.include_router(sample_router_v1.router)

# Override datetime encoder for the json response
ENCODERS_BY_TYPE[datetime] = to_epoch

# FastAPI pagination
add_pagination(app)

if __name__ == '__main__':
    config = app_config()
    port = config.port
    reload = config.environment == 'local'

    uvicorn.run('main:app', host='0.0.0.0', port=port, reload=reload)
