from app.core.clients.httpx_client import client
from app.core.configs.client_config import client_config
from app.core.logs.logging import get_logger

logger = get_logger(__name__)
_config = client_config()


async def home_page():
    sample_url = _config.sample_url

    logger.info(f"Viewing google homepage {sample_url}")

    response = await client().get(sample_url)

    return response.text
