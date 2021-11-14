from uuid import UUID

from app.api.v1.data.sample_in import SampleIn
from app.api.v1.data.sample_out import SampleOut
from app.api.v1.search import sample_search
from app.configs.constants import TOPIC_SAMPLE_CREATE
from app.core.events import kafka_producer
from app.core.exceptions.resource_not_found_exception import \
    ResourceNotFoundException
from app.models.sample import Sample
from app.models.sample_translation import SampleTranslation
from tortoise.transactions import in_transaction

RESOURCE_NAME = 'Sample'


async def get(id: UUID) -> SampleOut:
    sample = await Sample.filter(id=id) \
        .first() \
        .prefetch_related('translations')

    if not sample:
        raise ResourceNotFoundException(resource=RESOURCE_NAME, identifier=id)

    return SampleOut(**sample.dict())


async def save(sample_in: SampleIn) -> SampleOut:
    async with in_transaction() as connection:
        sample = await Sample.create(
            **sample_in.dict(exclude={'translations'}),
            column_1=sample_in.field_1,
            column_2=sample_in.field_2,
            using_db=connection
        )

        # Save the translations of the record
        await SampleTranslation.bulk_create(
            [
                SampleTranslation(**translation.dict(), sample=sample)
                for translation in sample_in.translations
            ],
            using_db=connection
        )

        # Get the result of the saved translations
        await sample.fetch_related('translations', using_db=connection)

        # Save the model to elasticsearch
        await sample_search.save(sample)

        # Send the data to kafka
        await kafka_producer.send(TOPIC_SAMPLE_CREATE, sample.kafka_dict())

    return SampleOut(**sample.dict())


async def delete(id: UUID) -> None:
    await Sample.filter(id=id).delete()
