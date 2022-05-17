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

        return [translation.dict() for translation in self.translations]

    async def sync_translations(
            self,
            translations: List[TranslationModel],
            using_db: Optional[BaseDBAsyncClient] = None
    ):
        deletes = await self._sync_current(translations, using_db)
        creates = await self._sync_new(translations)

        if creates:
            model = self.translations.remote_model

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

    async def _sync_current(
            self,
            translations: List[TranslationModel],
            using_db: Optional[BaseDBAsyncClient] = None
    ) -> List[TranslationModel]:
        deletes: List[TranslationModel] = []

        for current in self.translations:
            if current.language not in [n.language for n in translations]:
                deletes.append(current)

                continue

            for new in translations:
                if new.language == current.language:
                    await (
                        current
                            .update_from_dict({**new.dict(), "id": current.id})
                            .save(using_db=using_db)
                    )

        return deletes

    async def _sync_new(
            self,
            translations: List[TranslationModel]
    ) -> List[TranslationModel]:
        creates: List[TranslationModel] = []

        for new in translations:
            if new.language not in [c.language for c in self.translations]:
                creates.append(new)

                continue

        return creates
