from tortoise.fields import CharField, FloatField, ManyToManyField, UUIDField
from tortoise.fields.relational import ManyToManyRelation

from app.core.models.localized_model import LocalizedModel
from app.core.models.manager import DeletableManager
from app.core.models.model import AuditableMixin, DeletableMixin, SeekableMixin
from app.models.sample_translation import SampleTranslation


class Sample(LocalizedModel, SeekableMixin, AuditableMixin, DeletableMixin):
    id = UUIDField(pk=True)
    column_1 = CharField(max_length=150, unique=True, index=True)
    column_2 = CharField(null=True, max_length=1000)
    amount = FloatField(min=0.01, max=999999999.99)
    translations: ManyToManyRelation[SampleTranslation] = ManyToManyField(
        "app.SampleTranslation",
        through="sample_translation",
        backward_key="reference_id",
        forward_key="id"
    )

    class Meta:
        manager = DeletableManager()
