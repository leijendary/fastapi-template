from fastapi import FastAPI
from starlette_prometheus import metrics

from app.api.v1.routers import sample_router as sample_router_v1
from app.core.configs.app_config import app_config
from app.core.routers import healthcheck_router

_config = app_config()

# Routers
routers = [
    healthcheck_router.router,
    sample_router_v1.router,
]


def include_routers(app: FastAPI):
    [app.include_router(router, prefix=_config.prefix) for router in routers]

    app.add_route('/metrics/', metrics, include_in_schema=False)
