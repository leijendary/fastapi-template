from email.mime import base

from aiozipkin import CLIENT
from app.core.configs.client_config import client_config
from app.core.logs.logging import get_logger
from httpx import (AsyncClient, AsyncHTTPTransport, Auth, Headers, QueryParams,
                   Request, Response)
from starlette_zipkin import trace

logger = get_logger(__name__)
_config = client_config()
_retries = _config.retries


class TracingTransport(AsyncHTTPTransport):
    async def handle_async_request(self, request: Request) -> Response:
        url = request.url
        scheme = url.scheme
        method = request.method
        host = f"{url.host}:{url.port}" if url.port else url.host
        path = url.path
        name = f"{scheme} {method} {host}{path}"

        async with trace(name, CLIENT) as child_span:
            headers = child_span.make_headers()

            request.headers.update(headers)

        return await super().handle_async_request(request)


_transport = TracingTransport(http2=True, retries=_retries)


def async_client(
    base_url: str = None,
    auth: Auth = None,
    params: QueryParams = None,
    headers: Headers = None
) -> AsyncClient:
    return AsyncClient(
        base_url=base_url,
        auth=auth,
        params=params,
        headers=headers,
        http2=True,
        verify=False,
        trust_env=False,
        transport=_transport
    )
