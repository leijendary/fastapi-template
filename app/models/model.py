from app.utils.dict import to_dict
from tortoise.models import Model


class Model(Model):
    class Meta:
        abstract = True

    def dict(self):
        return to_dict(self)

    def kafka_data(self):
        return self.dict()
