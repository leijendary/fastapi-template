from typing import List, Optional

from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.fields.relational import ManyToManyRelation

from app.core.models.model import Model
from app.core.models.translation import TranslationModel


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

    async def sync_translations(
            self,
            translations: List[TranslationModel],
            using_db: Optional[BaseDBAsyncClient] = None
    ):
        creates = []
        deletes = []

        for c in self.translations:
            if c.language not in [n.language for n in translations]:
                deletes.append(c)

                continue

            for n in translations:
                if n.language == c.language:
                    c.update_from_dict({**n.dict(), "id": c.id})

                    await c.save(using_db=using_db)

        for n in translations:
            if n.language not in [c.language for c in self.translations]:
                creates.append(n)

                continue

        model = self.translations.remote_model

        if creates:
            await model.bulk_create(creates, using_db=using_db)

        if deletes:
            await self.translations.remove(*deletes, using_db=using_db)

    def dict(self):
        return {
            **super().dict(),
            **{"translations": self.translations_dict()}
        }

    def kafka_dict(self):
        return {
            **super().kafka_dict(),
            **{"translations": self.translations_dict()}
        }
