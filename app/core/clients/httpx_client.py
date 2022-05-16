from httpx import AsyncClient, Auth, Headers, QueryParams, AsyncHTTPTransport
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor, \
    AsyncOpenTelemetryTransport

HTTPXClientInstrumentor().instrument()

_transport = AsyncOpenTelemetryTransport(AsyncHTTPTransport())


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
