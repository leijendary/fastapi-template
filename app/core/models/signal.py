from typing import List, Optional, Type

from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.signals import pre_save

from app.core.context.request_context import current_user
from app.core.models.model import AuditableMixin


def init():
    auditables()


def auditables():
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
