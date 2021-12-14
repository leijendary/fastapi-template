from app.api.v1.data.sample_search_out import SampleSearchOut
from app.configs.constants import INDEX_SAMPLE
from app.core.context.elasticsearch_context import ElasticsearchContext
from app.core.data.params import SortParams
from app.core.utils.search_util import map_type, to_page, translation_page
from app.models.sample import Sample

RESOURCE_NAME = "Sample Document"


async def list(query, params: SortParams, locale):
    fields = ["translations.name", "translations.description"]
    body = translation_page(query, params, fields)
    result = await ElasticsearchContext.instance.search(
        index=INDEX_SAMPLE,
        body=body
    )

    return to_page(result, params, SampleSearchOut, locale)


async def get(id, locale):
    result = await ElasticsearchContext.instance.get(index=INDEX_SAMPLE, id=id)

    return map_type(result, SampleSearchOut, locale)


async def save(sample: Sample):
    document = mapping(sample)

    # Save the object in elasticsearch
    await ElasticsearchContext.instance.index(
        index=INDEX_SAMPLE,
        document=document,
        id=sample.id
    )


async def update(sample: Sample):
    document = mapping(sample)

    # Update the object in elasticsearch
    await ElasticsearchContext.instance.update(
        index=INDEX_SAMPLE,
        document=document,
        id=sample.id
    )


async def delete(id):
    # Delete the object from elasticsearch
    await ElasticsearchContext.instance.delete(index=INDEX_SAMPLE, id=id)


def mapping(sample: Sample):
    return {
        "column_1": sample.column_1,
        "column_2": sample.column_2,
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
