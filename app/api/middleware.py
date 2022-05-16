from fastapi import FastAPI
from starlette_context.middleware.raw_middleware import RawContextMiddleware
from starlette_prometheus import PrometheusMiddleware
from starlette_zipkin import ZipkinMiddleware, ZipkinConfig

from app.core.configs.app_config import app_config
from app.core.configs.monitoring_config import monitoring_config
from app.core.plugins.request_plugin import (AuthorizationPlugin,
                                             LanguagePlugin, UserPlugin)

_app_config = app_config()
_monitoring_config = monitoring_config()

middlewares = {
    RawContextMiddleware: {
        "plugins": [
            AuthorizationPlugin(),
            UserPlugin(),
            LanguagePlugin()
        ]
    },
    PrometheusMiddleware: {},
    ZipkinMiddleware: {
        "config": ZipkinConfig(
            host=_monitoring_config.host,
            port=_monitoring_config.port,
            service_name=_app_config.name,
            sample_rate=_monitoring_config.sample_rate,
            inject_response_headers=_monitoring_config.inject_response_headers,
            force_new_trace=_monitoring_config.force_new_trace
        )
    }
}


def add_middlewares(app: FastAPI):
    [
        app.add_middleware(middleware, **options)
        for middleware, options in middlewares.items()
    ]
