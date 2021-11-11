from app.models.localized_model import LocalizedModel
from app.models.sample_translation import SampleTranslation
from tortoise.fields import (CharField, DatetimeField, ManyToManyField,
                             UUIDField)
from tortoise.fields.relational import ManyToManyRelation


class Sample(LocalizedModel):
    id = UUIDField(pk=True)
    column_1 = CharField(max_length=150)
    column_2 = CharField(null=True, max_length=1000)
    translations: ManyToManyRelation[SampleTranslation] = ManyToManyField(
        'app.SampleTranslation',
        through='sample_translation',
        backward_key='sample_id',
        forward_key='id'
    )
    created_at = DatetimeField(auto_now_add=True)
    modified_at = DatetimeField(auto_now=True)
    deleted_at = DatetimeField(null=True)
