from typing import Optional

from app.core.data.translation_out import TranslationOut


class SampleTranslationOut(TranslationOut):
    name: str
    description: Optional[str]
