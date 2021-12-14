from typing import List, Optional, Type

from app.core.context.request_context import current_user
from app.core.models.model import AuditableMixin, DeletableMixin
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.signals import pre_save

for subclass in AuditableMixin.__subclasses__():
    @pre_save(subclass)
    async def auditable_pre_save(
        sender: Type[subclass],
        instance: subclass,
        using_db: Optional[BaseDBAsyncClient],
        update_fields: List[str]
    ):
        user = current_user()

        if instance._saved_in_db:
            instance.modified_by = user
        else:
            instance.created_by = user
            instance.modified_by = user


for subclass in DeletableMixin.__subclasses__():
    @pre_save(subclass)
    async def deletable_pre_save(
        sender: Type[subclass],
        instance: subclass,
        using_db: Optional[BaseDBAsyncClient],
        update_fields: List[str]
    ):
        if instance.deleted_at:
            user = current_user()

            instance.deleted_by = user
