from inspect import Parameter, signature
from typing import Type

from app.core.utils.dict_util import to_dict
from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import ModelField
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


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for _, model_field in cls.__fields__.items():
        model_field: ModelField

        if not model_field.required:
            new_parameters.append(
                Parameter(
                    model_field.alias,
                    Parameter.POSITIONAL_ONLY,
                    default=Form(model_field.default),
                    annotation=model_field.outer_type_,
                )
            )
        else:
            new_parameters.append(
                Parameter(
                    model_field.alias,
                    Parameter.POSITIONAL_ONLY,
                    default=Form(...),
                    annotation=model_field.outer_type_,
                )
            )

    def as_form_func(**data):
        return cls(**data)

    sig = signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig

    setattr(cls, 'as_form', as_form_func)

    return cls
