from datetime import datetime
from typing import List
from uuid import UUID

from app.api.v1.data.sample_translation_out import SampleTranslationOut
from app.core.libraries.message import get_message
from pydantic import BaseModel
from pydantic.fields import Field


class SampleOut(BaseModel):
    id: UUID
    column_1: str = Field(
        ...,
        title=get_message('document.sample_column_1'),
        max_length=100
    )
    column_2: str = Field(..., title=get_message('document.sample_column_2'))
    translations: List[SampleTranslationOut] = Field(
        [],
        title=get_message('document.translation_list'),
        min_items=1,
        unique_list=True
    )
    created_at: datetime = Field(..., title=get_message('document.created_at'))
    modified_at: datetime = Field(
        ...,
        title=get_message('document.modified_at')
    )
