from typing import Any, List

from pydantic import Field
from pydantic.main import BaseModel


class ErrorSource(BaseModel):
    sources: List[Any] = Field(...)
    code: str = ''
    message: str = ''
