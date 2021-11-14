from app.core.logs.logging import get_logger
from httpx import AsyncClient

logger = get_logger(__name__)

client = AsyncClient()


async def close():
    logger.info('Closing http client...')

    await client.aclose()

    logger.info('Http client closed!')
