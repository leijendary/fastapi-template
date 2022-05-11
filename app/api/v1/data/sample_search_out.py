from datetime import datetime
from uuid import UUID

from app.core.data.search_out import SearchOut


class SampleSearchOut(SearchOut):
    id: UUID
    column_1: str
    column_2: str
    amount: float = None
    name: str = ""
    description: str = ""
    created_at: datetime
