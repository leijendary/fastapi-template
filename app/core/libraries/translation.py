import json
import os
from functools import lru_cache

from app.core.configs.app_config import app_config
from app.core.context.request_context import current_language

_config = app_config()
_internationalization_path = _config.internationalization_path
_language_default = _config.language_default


@lru_cache
def load_translation():
    translation = {}

    for file_name in [
        file for file in os.listdir(_internationalization_path)
        if file.endswith(".json")
    ]:
        with open(_internationalization_path + file_name) as json_file:
            lang = file_name.split(".")[1]
            translation[lang] = json.load(json_file)

    return translation


def translate(code: str, language=current_language()):
    translation = load_translation()

    if language not in translation:
        language = _language_default

    locale = translation[language]

    if code not in locale:
        return code

    return locale[code]
