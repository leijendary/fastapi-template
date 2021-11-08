import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from tortoise.exceptions import IntegrityError

from app.configs import database
from app.configs.app import app_config
from app.data.error_response import ErrorResponse
from app.errors.integrity import integrity_handler
from app.errors.validation import validation_handler
from app.v1.routers import sample_router as sample_router_v1


def get_application():
    # App instance
    app = FastAPI(
        title='FastAPI Template',
        version='0.0.1',
        responses={
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

    # Configurations
    database.init(app)

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

    uvicorn.run("main:app", host='0.0.0.0', port=port, reload=reload)
