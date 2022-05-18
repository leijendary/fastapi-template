from typing import List
from uuid import UUID

from pydantic.fields import Field

from app.api.v1.data.sample_translation_out import SampleTranslationOut
from app.core.data.schema import TimestampSchema
from app.core.libraries.message import get_message


class SampleOut(TimestampSchema):
    id: UUID
    column_1: str = Field(
        ...,
        title=get_message("document.sample_column_1"),
        max_length=100
    )
    column_2: str = Field(..., title=get_message("document.sample_column_2"))
    amount: float = Field(..., title=get_message("document.sample_amount"))
    translations: List[SampleTranslationOut] = Field(
        ...,
        title=get_message("document.translation_list"),
    )
