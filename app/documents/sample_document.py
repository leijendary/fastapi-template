from app.constants import INDEX_SAMPLE
from app.core.search import elasticsearch_setup
from app.core.search.elasticsearch_settings import NGRAM_ANALYZER

sample = {
    "settings": NGRAM_ANALYZER,
    "mappings": {
        "properties": {
            "column_1": {
                "type": "text"
            },
            "column_2": {
                "type": "integer"
            },
            "amount": {
                "type": "double"
            },
            "created_at": {
                "type": "date",
                "format": "date_time"
            },
            "translations": {
                "type": "nested",
                "include_in_parent": True,
                "properties": {
                    "description": {
                        "type": "text"
                    },
                    "language": {
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "ngram_analyzer",
                        "search_analyzer": "standard"
                    },
                    "ordinal": {
                        "type": "integer"
                    }
                }
            }
        }
    }
}


async def init():
    await elasticsearch_setup.create_index(INDEX_SAMPLE, sample)
