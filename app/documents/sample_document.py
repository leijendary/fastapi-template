import json

from app.constants import INDEX_SAMPLE
from app.core.search import elasticsearch

sample = {
    "settings": json.load(
        open("app/core/search/ngram-analyzer.settings.json")
    ),
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
    await elasticsearch.create_index(INDEX_SAMPLE, sample)
