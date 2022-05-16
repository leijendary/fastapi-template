from typing import Optional

from pydantic import Field

from app.core.data.schema import TranslationSchema
from app.core.libraries.message import get_message


class SampleTranslationIn(TranslationSchema):
    name: str = Field(
        ...,
        title=get_message("document.translation_name"),
        min_length=1,
        max_length=150
    )
    description: Optional[str] = Field(
        None,
        title=get_message("document.translation_description"),
        min_length=1,
        max_length=1000
    )
