from tortoise.manager import Manager
from tortoise.queryset import QuerySet


class DeletableManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(deleted_at__isnull=True)
