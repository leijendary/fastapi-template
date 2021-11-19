from datetime import datetime
from uuid import UUID

from app.core.libraries.message import get_message
from pydantic.fields import Field
from pydantic.main import BaseModel


class SampleListOut(BaseModel):
    id: UUID
    column_1: str = Field(
        ...,
        title=get_message('document.sample_column_1'),
        max_length=100
    )
    column_2: str = Field(..., title=get_message('document.sample_column_2'))
    created_at: datetime = Field(..., title=get_message('document.created_at'))
    modified_at: datetime = Field(
        ...,
        title=get_message('document.modified_at')
    )
