from app.core.databases import main_sql
from app.models import sample, sample_translation

_models = [
    sample.__name__,
    sample_translation.__name__,
]


async def init():
    await main_sql.init(_models)
