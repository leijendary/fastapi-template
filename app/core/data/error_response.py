from datetime import datetime
from typing import List

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from .error_source import ErrorSource


class ErrorResponse(JSONResponse):
    def render(self, errors: List[ErrorSource], meta={}) -> bytes:
        content = {
            'errors': errors,
            'meta': {
                'status': self.status_code,
                'timestamp': datetime.utcnow(),
                **meta
            }
        }

        return super().render(jsonable_encoder(content))
