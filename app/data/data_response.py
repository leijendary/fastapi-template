from datetime import datetime
from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page
from starlette.responses import JSONResponse


class DataResponse(JSONResponse):
    data: Any
    meta: dict = {}

    def render(self, content: Any) -> bytes:
        meta = {
            'status': self.status_code,
            'timestamp': jsonable_encoder(datetime.utcnow()),
        }

        if isinstance(content, Page):
            meta = self.page_meta(content, meta)

            content = content.items

        content = {
            'data': {**content},
            'meta': meta
        }

        return super().render(content)

    def page_meta(self, content: Any, meta={}):
        return {
            **meta,
            'count': len(content.items),
            'total': content.total,
            'page': content.page,
            'size': content.size
        }
