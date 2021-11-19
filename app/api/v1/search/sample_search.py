from app.api.v1.data.sample_search_out import SampleSearchOut
from app.configs.constants import INDEX_SAMPLE
from app.core.data.params import SortParams
from app.core.search.elasticsearch import elasticsearch
from app.core.utils.search_util import to_page, translation_page
from app.models.sample import Sample


async def list(query, params: SortParams, locale):
    fields = ['translations.name', 'translations.description']
    body = translation_page(query, params, fields)
    result = await elasticsearch().search(index=INDEX_SAMPLE, body=body)

    return to_page(result, params, SampleSearchOut, locale)


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
    await elasticsearch().index(
        index=INDEX_SAMPLE,
        document=document,
        id=sample.id
    )
