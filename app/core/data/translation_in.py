from app.core.libraries.message import get_message
from pydantic import BaseModel, Field


class TranslationIn(BaseModel):
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