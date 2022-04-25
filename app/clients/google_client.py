from app.core.configs.client_config import client_config
from app.core.context.httpx_context import HttpxClientContext
from app.core.logs.logging import get_logger

logger = get_logger(__name__)
_config = client_config()


async def home_page():
    sample_url = _config.sample_url

    logger.info(f"Viewing google homepage {sample_url}")

    response = await HttpxClientContext.instance.get(sample_url)

    return response.text
