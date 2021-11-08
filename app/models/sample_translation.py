from app.models.translation import TranslationModel
from tortoise.contrib.pydantic.creator import pydantic_queryset_creator
from tortoise.fields import CharField
from tortoise.fields.relational import ForeignKeyField


class SampleTranslation(TranslationModel):
    sample = ForeignKeyField('app.Sample')
    name = CharField(max_length=150)
    description = CharField(null=True, max_length=1000)

    class Meta:
        table = 'sample_translation'
