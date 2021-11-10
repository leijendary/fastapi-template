from typing import Any, Generic, TypeVar

from app.models.app_model import AppModel
from tortoise.fields.relational import ManyToManyRelation


class LocalizedModel(AppModel):
    translations: ManyToManyRelation[Any]

    class Meta:
        abstract = True

    def translations_dict(self):
        return {
            'translations': [
                translation.dict()
                for translation in self.translations
            ]
        }

    def dict(self):
        return {**super().dict(), **self.translations_dict()}

    def kafka_dict(self):
        return {**super().kafka_data(), **self.translations_dict()}
