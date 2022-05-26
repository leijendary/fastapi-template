from datetime import datetime

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic.json import ENCODERS_BY_TYPE

from app import exception, shutdown, startup
from app.api import middleware, route
from app.core.configs.app_config import app_config
from app.core.data.data_response import DataResponse
from app.core.logs.logging_setup import get_logger
from app.core.utils.date_util import to_epoch

# Override datetime encoder for the json response
ENCODERS_BY_TYPE[datetime] = to_epoch

_app_config = app_config()
logger = get_logger(__name__)


def create_app() -> FastAPI:
    logger.info(f"Running in {_app_config.environment} environment")

    # App instance
    application = FastAPI(
        title=_app_config.name,
        version=_app_config.version,
        default_response_class=DataResponse,
    )

    startup.add_handlers(application)
    shutdown.add_handlers(application)
    middleware.add_middlewares(application)
    exception.add_handlers(application)
    route.include_routers(application)

    FastAPIInstrumentor.instrument_app(
        application,
        excluded_urls="healthcheck,metrics"
    )

    return application


# Create an instance of the app
app = create_app()
