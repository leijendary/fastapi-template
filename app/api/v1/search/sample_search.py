from app.configs.constants import INDEX_SAMPLE
from app.configs.elasticsearch_config import elasticsearch
from app.models.sample import Sample

_query = {
    "query": {
        "bool": {
            "should": [
                {
                    "match": {
                        "translations.name": {
                            "query": "{query}",
                            "fuzziness": "AUTO"
                        }
                    }
                },
                {
                    "match": {
                        "translations.description": {
                            "query": "{query}",
                            "fuzziness": "AUTO"
                        }
                    }
                }
            ]
        }
    },
    "sort": {
        "_score": {
            "order": "desc"
        }
    }
}


async def save(sample: Sample):
    document = {
        'column_1': sample.column_1,
        'column_2': sample.column_2,
        'created_at': sample.created_at,
        'translations': [
            {
                'name': translation.name,
                'description': translation.description,
                'language': translation.language,
                'ordinal': translation.ordinal,
            }
            for translation in sample.translations
        ]
    }

    # Save the object in elasticsearch
    result = await elasticsearch.index(INDEX_SAMPLE, document, id=sample.id)

    print(result)
