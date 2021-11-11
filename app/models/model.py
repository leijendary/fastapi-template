from app.utils.dict import to_dict
from tortoise.models import Model as TortoiseModel


class Model(TortoiseModel):
    class Meta:
        abstract = True

    def dict(self):
        return to_dict(self)

    def kafka_dict(self):
        return self.dict()
