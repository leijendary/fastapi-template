import json
import logging

from app.configs.constants import INDEX_SAMPLE
from app.configs.elasticsearch_config import elasticsearch_config
from app.core.context.elasticsearch_context import ElasticsearchContext
from app.core.logs.logging import get_logger

logger = get_logger(__name__)
_config = elasticsearch_config()

# Override elasticsearch log level
tracer = logging.getLogger("elasticsearch")
tracer.setLevel(_config.log_level)

indices = {
    INDEX_SAMPLE: {
        "settings": json.load(
            open("app/core/search/ngram-analyzer.settings.json")
        ),
        "mappings": json.load(
            open("app/core/search/sample.mapping.json")
        )
    }
}


async def init():
    logger.info("Initializing elasticsearch...")

    ElasticsearchContext.init(_config)

    await ElasticsearchContext.init_indices(indices)

    logger.info("Elasticsearch initialized!")


async def close():
    logger.info("Closing elasticsearch...")

    await ElasticsearchContext.close()

    logger.info("Elasticsearch closed!")
