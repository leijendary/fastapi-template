import json
import os
from functools import lru_cache

from app.core.configs.app_config import app_config

_config = app_config()
_message_path = _config.message_path


@lru_cache
def load_message():
    message = {}

    for file_name in [
        file for file in os.listdir(_message_path)
        if file.endswith(".json")
    ]:
        with open(_message_path + file_name) as json_file:
            lang = file_name.split(".")[0]
            message[lang] = json.load(json_file)

    return message


def get_message(code: str, *params):
    message = load_message()
    library, key = code.split(".")

    if library not in message:
        return code

    message = message[library]

    if key not in message:
        return code

    return message[key].format(*params)
