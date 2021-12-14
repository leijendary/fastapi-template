from app.core.models.translation import TranslationModel
from tortoise.fields import CharField
from tortoise.fields.relational import ForeignKeyField


class SampleTranslation(TranslationModel):
    reference = ForeignKeyField("app.Sample")
    name = CharField(max_length=150)
    description = CharField(null=True, max_length=1000)

    class Meta:
        table = "sample_translation"
