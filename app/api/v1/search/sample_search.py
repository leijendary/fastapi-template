from typing import Tuple, Iterable

from elasticsearch._async.helpers import async_bulk

from app.api.v1.data.sample_search_out import SampleSearchOut
from app.constants import INDEX_SAMPLE, RESOURCE_SAMPLE_DOCUMENT
from app.core.data.params import SortParams
from app.core.exceptions.resource_not_found_exception import \
    ResourceNotFoundException
from app.core.search.elasticsearch_setup import elasticsearch
from app.core.utils.search_util import map_type, to_page, translation_page
from app.models.sample import Sample


async def list(query, params: SortParams):
    fields = ["translations.name", "translations.description"]
    body = translation_page(query, params, fields)
    result = await elasticsearch().search(index=INDEX_SAMPLE, body=body)

    return to_page(result, params, SampleSearchOut)


async def get(id):
    result = await elasticsearch().get(index=INDEX_SAMPLE, id=id)

    if not result:
        raise ResourceNotFoundException(RESOURCE_SAMPLE_DOCUMENT, id)

    return map_type(result, SampleSearchOut)


async def save(sample: Sample):
    document = mapping(sample)

    # Save the object in elasticsearch
    await elasticsearch().index(
        index=INDEX_SAMPLE,
        body=document,
        id=sample.id
    )


async def save_bulk(samples: Iterable[Sample]) -> Tuple[int, int]:
    actions = [
        {
            "_index": INDEX_SAMPLE,
            "_id": sample.id,
            "_source": mapping(sample)
        }
        for sample in samples
    ]

    return await async_bulk(elasticsearch(), actions, stats_only=True)


async def update(sample: Sample):
    document = mapping(sample)

    # Update the object in elasticsearch
    await elasticsearch().index(
        index=INDEX_SAMPLE,
        body=document,
        id=sample.id
    )


async def delete(id):
    # Delete the object from elasticsearch
    await elasticsearch().delete(index=INDEX_SAMPLE, id=id)


def mapping(sample: Sample):
    return {
        "column_1": sample.column_1,
        "column_2": sample.column_2,
        "amount": sample.amount,
        "created_at": sample.created_at,
        "translations": [
            {
                "name": translation.name,
                "description": translation.description,
                "language": translation.language,
                "ordinal": translation.ordinal,
            }
            for translation in sample.translations
        ]
    }
