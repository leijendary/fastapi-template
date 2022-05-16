from typing import Any

from pydantic.main import BaseModel

from app.core.utils.locale_util import localize


class SearchOut(BaseModel):
    def __init__(self, locale=None, **data: Any) -> None:
        if "translations" in data:
            translation = localize(locale, data["translations"])
            data = {**data, **translation}

        super().__init__(**data)
