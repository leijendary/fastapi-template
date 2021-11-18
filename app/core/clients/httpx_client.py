from app.core.context.httpx_context import HttpxClientContext
from app.core.logs.logging import get_logger

logger = get_logger(__name__)


async def init():
    logger.info('Initializing http client...')

    HttpxClientContext.init()

    logger.info('Http client initialized!')


async def close():
    logger.info('Closing http client...')

    await HttpxClientContext.close()

    logger.info('Http client closed!')

def client():
    return HttpxClientContext.instance
