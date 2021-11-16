from typing import Any

from app.configs.app_config import app_config
from app.core.utils.locale_util import localize
from pydantic.main import BaseModel

_app_config = app_config()
language_default = _app_config.language_default


class SearchOut(BaseModel):
    def __init__(self, data: Any, locale) -> None:
        locale = locale if locale else language_default

        if 'translations' in data:
            translation = localize(locale, data['translations'])

            data = {**data, **translation}

        super().__init__(**data)
