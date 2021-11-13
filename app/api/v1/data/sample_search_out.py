from datetime import datetime

from app.core.data.search_out import SearchOut


class SampleSearchOut(SearchOut):
    column_1: str
    column_2: str
    name: str = ''
    description: str = ''
    created_at: datetime
