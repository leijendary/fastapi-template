from datetime import date, datetime
from uuid import UUID


def to_dict(obj):
    if not hasattr(obj, "__dict__"):
        return obj

    result = {}

    for key, val in obj.__dict__.items():
        if key.startswith("_"):
            continue

        element = []

        if isinstance(val, list):
            for item in val:
                element.append(to_dict(item))
        elif isinstance(val, (datetime, date)):
            element = val.isoformat()
        elif isinstance(val, UUID):
            element = str(val)
        else:
            element = to_dict(val)

        result[key] = element

    return result
