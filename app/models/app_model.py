from tortoise.models import Model


class AppModel(Model):
    class Meta:
        abstract = True

    def dict(self):
        return self.__dict__
