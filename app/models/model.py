from app.core.databases import postgres_setup
from app.models import sample, sample_translation

_models = [
    sample.__name__,
    sample_translation.__name__,
]


async def init():
    await postgres_setup.init(_models)
