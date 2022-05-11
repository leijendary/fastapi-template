from app.core.logs.logging import get_logger
from httpx import AsyncClient

logger = get_logger(__name__)
client: AsyncClient = None


class Client:
    instance: AsyncClient

    @classmethod
    def init(self):
        self.instance = AsyncClient(http2=True)


def client() -> AsyncClient:
    return Client.instance


def init():
    logger.info("Initializing http client...")

    Client.init()

    logger.info("Http client initialized!")


async def close():
    logger.info("Closing http client...")

    await client().aclose()

    logger.info("Http client closed!")
