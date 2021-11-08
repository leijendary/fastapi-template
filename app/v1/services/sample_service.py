from app.models.sample import Sample
from app.models.sample_translation import SampleTranslation
from app.v1.data.sample_in import SampleIn
from app.v1.data.sample_out import SampleOut
from app.v1.data.sample_translation_out import SampleTranslationOut
from tortoise.transactions import in_transaction


async def page():
    pass


async def save(sample_in: SampleIn) -> SampleOut:
    async with in_transaction() as connection:
        sample = await Sample.create(
            **sample_in.dict(exclude={'translations'}),
            column_1=sample_in.field_1,
            column_2=sample_in.field_2,
            using_db=connection
        )

        # Save the translations of the record
        await SampleTranslation.bulk_create(
            [
                SampleTranslation(**translation.dict(), sample=sample)
                for translation in sample_in.translations
            ],
            using_db=connection
        )

    # Get the result of the saved translations
    await sample.fetch_related('translations')

    return SampleOut(**sample.dict(), translations=[
        SampleTranslationOut(**translation.dict())
        for translation in sample.translations
    ])
