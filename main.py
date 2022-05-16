from datetime import datetime

import uvicorn
from fastapi import FastAPI
from pydantic.json import ENCODERS_BY_TYPE

from app import exception, shutdown, startup
from app.api import middleware, route
from app.core.configs.app_config import app_config
from app.core.configs.logging_config import logging_config
from app.core.configs.security_config import security_config
from app.core.data.data_response import DataResponse
from app.core.utils.date_util import to_epoch

# Override datetime encoder for the json response
ENCODERS_BY_TYPE[datetime] = to_epoch

_config = app_config()


def create_app() -> FastAPI:
    # App instance
    app = FastAPI(
        title=_config.name,
        version=_config.version,
        default_response_class=DataResponse,
    )

    startup.add_handlers(app)
    shutdown.add_handlers(app)
    exception.add_handlers(app)
    middleware.add_middlewares(app)
    route.include_routers(app)

    return app


# Create an instance of the app
app = create_app()

if __name__ == "__main__":
    security = security_config()
    log = logging_config()
    reload = _config.environment == "local"

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=_config.port,
        reload=reload,
        access_log=log.access,
        use_colors=False,
        ssl_certfile=security.ssl_certfile,
        ssl_keyfile=security.ssl_keyfile,
        server_header=False
    )
