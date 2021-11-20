from app.core.utils.dict_util import to_dict
from tortoise.fields import DatetimeField
from tortoise.models import Model as TortoiseModel


class Model(TortoiseModel):
    class Meta:
        abstract = True

    def dict(self):
        return to_dict(self)

    def kafka_dict(self):
        return self.dict()


class TimestampMixin:
    created_at = DatetimeField(auto_now_add=True)
    modified_at = DatetimeField(auto_now=True)


class DeletableMixin:
    deleted_at = DatetimeField(null=True)
