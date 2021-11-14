from app.api.v1.data.sample_search_out import SampleSearchOut
from app.configs.constants import INDEX_SAMPLE
from app.core.search.elasticsearch import elasticsearch
from app.models.sample import Sample
from app.core.utils.search_util import to_page, translation_page


async def page(locale, query='', page: int = 1, size: int = 10, sort=None):
    fields = ['translations.name', 'translations.description']
    body = translation_page(query, fields, page, size, sort)
    result = await elasticsearch.search(body, INDEX_SAMPLE)

    return to_page(result, page, size, SampleSearchOut, locale)


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
    await elasticsearch.index(INDEX_SAMPLE, document, id=sample.id)
