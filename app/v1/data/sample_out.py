from datetime import datetime
from typing import List
from uuid import UUID

from app.v1.data.sample_translation_out import SampleTranslationOut
from pydantic import BaseModel


class SampleOut(BaseModel):
    id: UUID
    column_1: str
    column_2: str
    translations: List[SampleTranslationOut] = []
    created_at: datetime
    modified_at: datetime
