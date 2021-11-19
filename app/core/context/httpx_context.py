from httpx import AsyncClient


class HttpxClientContext:
    instance: AsyncClient

    @classmethod
    def init(cls):
        cls.instance = AsyncClient(http2=True)

    @classmethod
    async def close(cls):
        cls.instance.aclose()
