from app.models.app_model import AppModel
from tortoise.fields import CharField, IntField, SmallIntField


class TranslationModel(AppModel):
    id = IntField(pk=True)
    language = CharField(max_length=2)
    ordinal = SmallIntField(min=1)

    class Meta:
        abstract = True
