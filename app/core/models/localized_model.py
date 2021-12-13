from typing import List

from app.core.models.translation import TranslationModel
from tortoise.fields.relational import ManyToManyRelation

from .model import Model


class LocalizedModel(Model):
    translations: ManyToManyRelation[TranslationModel]

    class Meta:
        abstract = True

    def translations_dict(self):
        if not self.translations.related_objects:
            return []

        return [
            translation.dict()
            for translation in self.translations
        ]

    async def sync_translations(self, translations: List[TranslationModel]):
        creates = []
        deletes = []

        for c in self.translations:
            if c.language not in [n.language for n in translations]:
                deletes.append(c)

                continue

            for n in translations:
                if n.language == c.language:
                    c.update_from_dict({**n.dict(), 'id': c.id})

                    await c.save()

        for n in translations:
            if n.language not in [c.language for c in self.translations]:
                creates.append(n)

                continue

        model = self.translations.remote_model

        if creates:
            await model.bulk_create(creates)

        if deletes:
            await self.translations.remove(*deletes)

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
