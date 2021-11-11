from typing import Any

from app.models.model import Model
from tortoise.fields.relational import ManyToManyRelation


class LocalizedModel(Model):
    translations: ManyToManyRelation[Any]

    class Meta:
        abstract = True

    def translations_dict(self):
        return [
            translation.dict()
            for translation in self.translations
        ]

    def dict(self):
        return {
            **super().dict(),
            **{'translations': self.translations_dict()}
        }

    def kafka_dict(self):
        return {
            **super().kafka_dict(),
            **{'translations': self.translations_dict()}
        }
