from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic.json import ENCODERS_BY_TYPE
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.api.v1.routers import sample_router as sample_router_v1
from app.configs import database
from app.configs.app import app_config
from app.data.data_response import DataResponse
from app.data.error_response import ErrorResponse
from app.errors.integrity_error import integrity_handler
from app.errors.not_exists_error import not_exists_handler
from app.errors.not_found_error import not_found_handler
from app.errors.validation_error import validation_handler
from app.events.consumers import consumer
from app.utils.date import to_epoch

# Override datetime encoder for the json response
ENCODERS_BY_TYPE[datetime] = to_epoch


def get_application():
    # App instance
    app = FastAPI(
        title='FastAPI Template',
        version='0.0.1',
        responses={
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
    )

    # Event handlers
    app.add_event_handler('startup', database.init)
    app.add_event_handler('shutdown', database.close)
    app.add_event_handler('startup', consumer.init)

    # Exception handlers
    app.add_exception_handler(404, not_found_handler)
    app.add_exception_handler(DoesNotExist, not_exists_handler)
    app.add_exception_handler(IntegrityError, integrity_handler)
    app.add_exception_handler(RequestValidationError, validation_handler)

    # Routers
    app.include_router(sample_router_v1.router)

    return app


app = get_application()

if __name__ == '__main__':
    config = app_config()
    port = config.port
    reload = config.environment == 'local'

    uvicorn.run('main:app', host='0.0.0.0', port=port, reload=reload)
