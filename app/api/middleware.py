from app.core.plugins.request_plugin import AuthorizationPlugin, LanguagePlugin
from fastapi import FastAPI
from starlette_context.middleware.raw_middleware import RawContextMiddleware
from starlette_prometheus import PrometheusMiddleware

middlewares = {
    RawContextMiddleware: {
        "plugins": [
            AuthorizationPlugin(),
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
