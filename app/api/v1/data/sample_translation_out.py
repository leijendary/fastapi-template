from typing import Optional

from app.data.translation_out import TranslationOut


class SampleTranslationOut(TranslationOut):
    name: str
    description: Optional[str]
