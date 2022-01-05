from datetime import datetime
from typing import Any, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

T = TypeVar("T")


class DataResponse(JSONResponse):
    def render(self, data: Any, meta={"type": "object"}) -> bytes:
        if data and set({"items", "total", "page", "size"}) <= set(data):
            meta = page_meta(data, meta)
            data = data["items"]

        if (isinstance(data, list)):
            meta["type"] = "array"

        content = {
            "data": data,
            "meta": {
                "status": self.status_code,
                "timestamp": datetime.utcnow(),
                **meta
            }
        }

        return super().render(jsonable_encoder(content))


def page_meta(data: T, meta={}):
    return {
        **meta,
        "count": len(data["items"]),
        "total": data["total"],
        "page": data["page"],
        "size": data["size"]
    }
