from datetime import datetime

from app.core.libraries.message import get_message
from app.core.utils.date_util import to_epoch
from pydantic.fields import Field
from pydantic.main import BaseModel


class TranslationSchema(BaseModel):
    language: str = Field(
        ...,
        title=get_message('document.translation_language'),
        min_length=2,
        max_length=2
    )
    ordinal: int = Field(
        ...,
        title=get_message('document.translation_ordinal'),
        gt=0
    )


class TimestampSchema(BaseModel):
    created_at: datetime = Field(
        ...,
        title=get_message('document.created_at'),
        example=to_epoch(datetime.utcnow())
    )
    modified_at: datetime = Field(
        ...,
        title=get_message('document.modified_at'),
        example=to_epoch(datetime.utcnow())
    )
