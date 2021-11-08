from typing import Any, List

from pydantic.main import BaseModel


class ErrorSource(BaseModel):
    sources: List[Any] = []
    code: str = ''
    message: str = ''
