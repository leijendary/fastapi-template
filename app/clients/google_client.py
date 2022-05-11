from app.core.clients.httpx_client import client
from app.core.configs.client_config import client_config
from app.core.logs.logging import get_logger

logger = get_logger(__name__)
_config = client_config()
_sample_url = _config.sample_url


async def home_page():
    logger.info(f"Viewing google homepage {_sample_url}")

    response = await client().get(_sample_url)

    return response.text
