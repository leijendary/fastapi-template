from time import time
from typing import List, Dict
from uuid import UUID

from fastapi.datastructures import UploadFile
from starlette.websockets import WebSocket
from tortoise.expressions import Q
from tortoise.transactions import in_transaction

from app.api.v1.data.sample_in import SampleIn
from app.api.v1.data.sample_list_out import SampleListOut
from app.api.v1.data.sample_out import SampleOut
from app.api.v1.data.sample_translation_in import SampleTranslationIn
from app.api.v1.search import sample_search
from app.constants import (RESOURCE_SAMPLE, TOPIC_SAMPLE_CREATE,
                           TOPIC_SAMPLE_DELETE)
from app.core.constants import CONNECTION_PRIMARY
from app.core.data.file_stream import FileStream
from app.core.data.params import SeekParams
from app.core.data.seek import Seek
from app.core.exceptions.resource_not_found_exception import \
    ResourceNotFoundException
from app.core.messaging.kafka_setup import producer
from app.core.models.model import to_seek
from app.core.storages import s3_storage
from app.core.utils.file_util import get_name
from app.core.utils.websocket_util import redis_subscribe
from app.models.sample import Sample
from app.models.sample_translation import SampleTranslation

_FIELDS_FOR_SELECT = [
    "id",
    "row_id",
    "column_1",
    "column_2",
    "amount",
    "created_by",
    "created_at",
    "modified_by",
    "modified_at"
]
_EXCLUSIONS = {"field_1", "field_2", "translations"}
_TRANSLATIONS = "translations"


async def listen(websocket: WebSocket, cache_key: str, id: UUID):
    key = f"{cache_key}:{id}"

    await redis_subscribe(websocket, key)


async def seek(query, params: SeekParams) -> Seek[SampleListOut]:
    q = Q(
        Q(column_1__icontains=query),
        Q(column_2__icontains=query),
        Q(translations__name__icontains=query),
        Q(translations__description__icontains=query),
        join_type=Q.OR
    )
    queryset = (
        Sample
            .filter(q)
            .only(*_FIELDS_FOR_SELECT)
            .distinct()
    )

    return await to_seek(queryset, params, SampleListOut)


async def get(id: UUID) -> SampleOut:
    sample = await (
        Sample
            .filter(id=id)
            .only(*_FIELDS_FOR_SELECT)
            .prefetch_related(_TRANSLATIONS)
            .first()
    )

    if not sample:
        raise ResourceNotFoundException(RESOURCE_SAMPLE, id)

    return SampleOut(**sample.dict())


async def save(sample_in: SampleIn) -> SampleOut:
    async with in_transaction(CONNECTION_PRIMARY) as connection:
        sample = await Sample.create(**mapping(sample_in), using_db=connection)
        translations = mapping_translations(sample, sample_in.translations)

        # Create the translations
        await SampleTranslation.bulk_create(translations, using_db=connection)

        # Fetch the related models for returns
        await sample.fetch_related(_TRANSLATIONS, using_db=connection)

    # Save the model to elasticsearch
    await sample_search.save(sample)

    # Send the data to kafka
    await producer().send(TOPIC_SAMPLE_CREATE, sample.kafka_dict())

    return SampleOut(**sample.dict())


async def update(id: UUID, sample_in: SampleIn) -> SampleOut:
    sample = await (
        Sample
            .select_for_update()
            .filter(id=id)
            .prefetch_related(_TRANSLATIONS)
            .first()
    )

    if not sample:
        raise ResourceNotFoundException(RESOURCE_SAMPLE, id)

    async with in_transaction(CONNECTION_PRIMARY) as connection:
        # Update the instance from the database
        await (
            sample
                .update_from_dict(mapping(sample_in))
                .save(using_db=connection)
        )

        translations = mapping_translations(sample, sample_in.translations)

        # Sync the translations of the reference table
        await sample.sync_translations(translations, using_db=connection)

        # Fetch the related models for returns
        await sample.fetch_related(_TRANSLATIONS, using_db=connection)

    # Update the model in elasticsearch
    await sample_search.update(sample)

    # Send the data to kafka
    await producer().send(TOPIC_SAMPLE_CREATE, sample.kafka_dict())

    return SampleOut(**sample.dict())


async def delete(id: UUID) -> None:
    sample = await Sample.select_for_update().filter(id=id).first()

    if not sample:
        raise ResourceNotFoundException(RESOURCE_SAMPLE, id)

    await sample.soft_delete()

    # Delete the document from elasticsearch
    await sample_search.delete(id)

    # Send the data to kafka
    await producer().send(TOPIC_SAMPLE_DELETE, {"id": str(id)})


async def reindex() -> Dict:
    result = await Sample.all().prefetch_related(_TRANSLATIONS)
    start = time()
    success, failed = await sample_search.save_bulk(result)
    end = time()

    return {
        "success": success,
        "failed": failed,
        "time": end - start
    }


def file_download(bucket: str, folder: str, name: str) -> FileStream:
    return s3_storage.stream_response(bucket, f"{folder}/{name}")


def file_upload(bucket: str, folder: str, upload_file: UploadFile):
    name = get_name(upload_file.filename)
    key = f"{folder}/{name}"

    s3_storage.upload_file(
        upload_file.file,
        upload_file.content_type,
        bucket,
        key
    )

    return [key]


def file_delete(bucket: str, folder: str, name: str):
    s3_storage.delete_file(bucket, f"{folder}/{name}")


def mapping(sample_in: SampleIn):
    return {
        **sample_in.dict(exclude=_EXCLUSIONS),
        "column_1": sample_in.field_1,
        "column_2": sample_in.field_2,
    }


def mapping_translations(
        sample: Sample,
        translations: List[SampleTranslationIn]
):
    return [
        SampleTranslation(**translation.dict(), reference=sample)
        for translation in translations
    ]
