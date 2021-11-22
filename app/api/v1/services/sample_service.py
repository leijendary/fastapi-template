from datetime import datetime
from typing import List
from uuid import UUID

from app.api.v1.data.sample_in import SampleIn
from app.api.v1.data.sample_list_out import SampleListOut
from app.api.v1.data.sample_out import SampleOut
from app.api.v1.data.sample_translation_in import SampleTranslationIn
from app.api.v1.search import sample_search
from app.configs.constants import TOPIC_SAMPLE_CREATE, TOPIC_SAMPLE_DELETE
from app.core.data.params import SortParams
from app.core.events import kafka_producer
from app.core.exceptions.resource_not_found_exception import \
    ResourceNotFoundException
from app.core.utils.model_util import to_page
from app.models.sample import Sample
from app.models.sample_translation import SampleTranslation
from fastapi_pagination.default import Page
from tortoise.query_utils import Q
from tortoise.transactions import in_transaction

FIELDS_FOR_SELECT = ['id', 'column_1', 'column_2', 'created_at', 'modified_at']
EXCLUSIONS = {'field_1', 'field_2', 'translations'}
RESOURCE_NAME = 'Sample'


async def list(query, params: SortParams) -> Page[SampleListOut]:
    filter = Q(
        Q(column_1__icontains=query),
        Q(column_2__icontains=query),
        join_type='OR'
    )
    query = Sample.filter(filter).only(*FIELDS_FOR_SELECT)

    return await to_page(query, params, SampleListOut)


async def get(id: UUID) -> SampleOut:
    sample = await Sample.filter(id=id) \
        .only(*FIELDS_FOR_SELECT) \
        .prefetch_related('translations') \
        .first()

    if not sample:
        raise ResourceNotFoundException(resource=RESOURCE_NAME, identifier=id)

    return SampleOut(**sample.dict())


async def save(sample_in: SampleIn) -> SampleOut:
    async with in_transaction() as connection:
        sample = await Sample.create(**mapping(sample_in), using_db=connection)
        translations = mapping_translations(sample, sample_in.translations)

        # Create the translations
        await SampleTranslation.bulk_create(translations, using_db=connection)

        # Fetch the related models for returns
        await sample.fetch_related('translations', using_db=connection)

        # Save the model to elasticsearch
        await sample_search.save(sample)

        # Send the data to kafka
        await kafka_producer.send(TOPIC_SAMPLE_CREATE, sample.kafka_dict())

    return SampleOut(**sample.dict())


async def update(id: UUID, sample_in: SampleIn) -> SampleOut:
    sample = await Sample.filter(id=id) \
        .prefetch_related('translations') \
        .first()

    if not sample:
        raise ResourceNotFoundException(resource=RESOURCE_NAME, identifier=id)

    async with in_transaction() as connection:
        # Update the instance from the database
        await sample.update_from_dict(mapping(sample_in)).save(connection)

        translations = mapping_translations(sample, sample_in.translations)

        # Sync the translations of the reference table
        await sample.sync_translations(translations, connection)

        # Fetch the related models for returns
        await sample.fetch_related('translations', using_db=connection)

        # Update the model in elasticsearch
        await sample_search.save(sample)

        # Send the data to kafka
        await kafka_producer.send(TOPIC_SAMPLE_CREATE, sample.kafka_dict())

    return SampleOut(**sample.dict())


async def delete(id: UUID) -> None:
    sample = await Sample.filter(id=id).first()

    if not sample:
        raise ResourceNotFoundException(resource=RESOURCE_NAME, identifier=id)

    async with in_transaction() as connection:
        sample.deleted_at = datetime.now()

        await sample.save(using_db=connection)

        # Delete the document from elasticsearch
        await sample_search.delete(id)

        # Send the data to kafka
        await kafka_producer.send(TOPIC_SAMPLE_DELETE, {'id': str(id)})


def mapping(sample_in: SampleIn):
    return {
        **sample_in.dict(exclude=EXCLUSIONS),
        'column_1': sample_in.field_1,
        'column_2': sample_in.field_2,
    }


def mapping_translations(
    sample: Sample,
    translations: List[SampleTranslationIn]
):
    return [
        SampleTranslation(**translation.dict(), reference=sample)
        for translation in translations
    ]
