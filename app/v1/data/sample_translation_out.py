from typing import Optional

from app.data.translation_request import TranslationRequest


class SampleTranslationOut(TranslationRequest):
    name: str
    description: Optional[str]
