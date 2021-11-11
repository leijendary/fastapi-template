from datetime import datetime

import pydantic
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic.json import ENCODERS_BY_TYPE
from tortoise.exceptions import IntegrityError

from app.configs import database
from app.configs.app import app_config
from app.data.data_response import DataResponse
from app.data.error_response import ErrorResponse
from app.errors.integrity import integrity_handler
from app.errors.validation import validation_handler
from app.events.consumers import consumer
from app.v1.routers import sample_router as sample_router_v1

# Override datetime encoder for the json response
ENCODERS_BY_TYPE[datetime] = lambda dt: int(dt.timestamp() * 1000)


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
    app.add_exception_handler(RequestValidationError, validation_handler)
    app.add_exception_handler(IntegrityError, integrity_handler)

    # Routers
    app.include_router(sample_router_v1.router)

    return app


app = get_application()

if __name__ == '__main__':
    config = app_config()
    port = config.port
    reload = config.environment == 'local'

    uvicorn.run('main:app', host='0.0.0.0', port=port, reload=reload)
