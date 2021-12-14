
from app.core.models.localized_model import LocalizedModel
from app.core.models.manager import DeletableManager
from app.core.models.model import AuditableMixin, DeletableMixin
from app.models.sample_translation import SampleTranslation
from tortoise.fields import CharField, ManyToManyField, UUIDField
from tortoise.fields.relational import ManyToManyRelation


class Sample(LocalizedModel, AuditableMixin, DeletableMixin):
    id = UUIDField(pk=True)
    column_1 = CharField(max_length=150)
    column_2 = CharField(null=True, max_length=1000)
    translations: ManyToManyRelation[SampleTranslation] = ManyToManyField(
        'app.SampleTranslation',
        through='sample_translation',
        backward_key='reference_id',
        forward_key='id'
    )

    class Meta:
        manager = DeletableManager()
