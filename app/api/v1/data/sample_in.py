from typing import List

from pydantic.fields import Field

from app.api.v1.data.sample_translation_in import SampleTranslationIn
from app.core.data.schema import Schema
from app.core.libraries.message import get_message


class SampleIn(Schema):
    field_1: str = Field(
        ...,
        title=get_message("document.sample_field_1"),
        min_length=1,
        max_length=100
    )
    field_2: int = Field(
        ...,
        title=get_message("document.sample_field_2"),
        gt=0
    )
    amount: float = Field(
        ...,
        title=get_message("document.sample_amount"),
        gt=0.01,
        le=9999999999.99
    )
    translations: List[SampleTranslationIn] = Field(
        ...,
        title=get_message("document.translation_list"),
        min_items=1
    )
