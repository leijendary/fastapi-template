from typing import Any

from app.core.utils.locale_util import localize
from pydantic.main import BaseModel


class SearchOut(BaseModel):
    def __init__(self, locale=None, **data: Any) -> None:
        if 'translations' in data:
            translation = localize(locale, data['translations'])
            data = {**data, **translation}

        super().__init__(**data)
