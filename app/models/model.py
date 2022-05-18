from app.core.databases import postgres_setup
from app.core.databases.postgres_setup import create_configuration
from app.models import sample, sample_translation

_models = [
    sample.__name__,
    sample_translation.__name__,
]
config = create_configuration(_models)


async def init():
    await postgres_setup.init(_models, config)
