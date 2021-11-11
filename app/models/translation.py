from app.models.model import Model
from tortoise.fields import CharField, IntField, SmallIntField


class TranslationModel(Model):
    id = IntField(pk=True)
    language = CharField(max_length=2)
    ordinal = SmallIntField(min=1)

    class Meta:
        abstract = True
