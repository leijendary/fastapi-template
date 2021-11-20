from tortoise.fields import CharField, IntField, SmallIntField
from tortoise.fields.relational import ForeignKeyField

from .model import Model


class TranslationModel(Model):
    id = IntField(pk=True)
    reference: ForeignKeyField
    language = CharField(max_length=2)
    ordinal = SmallIntField(min=1)

    class Meta:
        abstract = True
