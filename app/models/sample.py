from app.models.app_model import AppModel
from app.models.sample_translation import SampleTranslation
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields import (CharField, DatetimeField, ManyToManyField,
                             UUIDField)
from tortoise.fields.relational import ManyToManyRelation, ReverseRelation


class Sample(AppModel):
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
