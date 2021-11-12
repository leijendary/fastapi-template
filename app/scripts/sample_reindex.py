
from app.api.v1.search import sample_search
from app.models.sample import Sample


async def run():
    samples = await Sample.all().prefetch_related('translations')

    for sample in samples:
        await sample_search.save(sample)
