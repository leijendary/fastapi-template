from fastapi import FastAPI
from starlette_context.middleware.raw_middleware import RawContextMiddleware
from starlette_prometheus import PrometheusMiddleware

from app.core.plugins.request_plugin import (AuthorizationPlugin,
                                             LanguagePlugin, UserPlugin)

middlewares = {
    RawContextMiddleware: {
        "plugins": [
            AuthorizationPlugin(),
            UserPlugin(),
            LanguagePlugin()
        ]
    },
    PrometheusMiddleware: {}
}


def add_middlewares(app: FastAPI):
    [
        app.add_middleware(middleware, **options)
        for middleware, options in middlewares.items()
    ]
