from httpx import AsyncClient


class HttpxClientContext:
    instance: AsyncClient

    @classmethod
    def init(self):
        self.instance = AsyncClient(http2=True)

    @classmethod
    async def close(self):
        self.instance.aclose()
