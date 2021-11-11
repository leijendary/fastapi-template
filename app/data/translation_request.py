from app.resources.messages.message import get_message
from pydantic import BaseModel
from pydantic.fields import Field


class TranslationRequest(BaseModel):
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
