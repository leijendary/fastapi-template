from aiozipkin import CLIENT
from httpx import (AsyncClient, AsyncHTTPTransport, Auth, Headers, QueryParams,
                   Request, Response)
from starlette_zipkin import trace


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


_transport = TracingTransport(http2=True)


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
