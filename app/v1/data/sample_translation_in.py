from typing import Optional

from app.data.translation_request import TranslationRequest
from app.resources.messages.message import get_message
from pydantic import Field


class SampleTranslationIn(TranslationRequest):
    name: str = Field(
        ...,
        title=get_message('document.translation_name'),
        min_length=1,
        max_length=150
    )
    description: Optional[str] = Field(
        None,
        title=get_message('document.translation_description'),
        min_length=1,
        max_length=1000
    )
