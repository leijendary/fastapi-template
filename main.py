from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_pagination import add_pagination
from pydantic.error_wrappers import ValidationError
from pydantic.json import ENCODERS_BY_TYPE
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.api.v1.routers import sample_router as sample_router_v1
from app.configs import (client_config, database_config, elasticsearch_config,
                         kafka_config)
from app.configs.app_config import app_config
from app.data.data_response import DataResponse
from app.errors.exceptions.invalid_token_exception import InvalidTokenException
from app.errors.generic_error import generic_handler
from app.errors.integrity_error import integrity_handler
from app.errors.invalid_token import invalid_token_handler
from app.errors.not_exists_error import not_exists_handler
from app.errors.not_found_error import not_found_handler
from app.errors.validation_error import validation_handler
from app.utils.date_util import to_epoch

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
    database_config.init,
    kafka_config.init,
    elasticsearch_config.init
]

# Shutdown event
on_shutdown = [
    database_config.close,
    elasticsearch_config.close,
    client_config.close
]

# App instance
app = FastAPI(
    title='FastAPI Template',
    version='0.0.1',
    default_response_class=DataResponse,
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
