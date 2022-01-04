from datetime import datetime
from inspect import Parameter, signature
from typing import Iterable, Optional, Type

from app.core.context.request_context import current_user
from app.core.utils.dict_util import to_dict
from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import ModelField
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.fields import DatetimeField
from tortoise.fields.data import TextField
from tortoise.models import Model as TortoiseModel


class Model(TortoiseModel):
    class Meta:
        abstract = True

    def dict(self):
        return to_dict(self)

    def kafka_dict(self):
        return self.dict()


class AuditableMixin(TortoiseModel):
    created_by = TextField()
    created_at = DatetimeField(auto_now_add=True)
    modified_by = TextField()
    modified_at = DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class DeletableMixin(TortoiseModel):
    deleted_by = TextField(null=True)
    deleted_at = DatetimeField(null=True)

    class Meta:
        abstract = True

    async def soft_delete(
        self,
        using_db: Optional[BaseDBAsyncClient] = None,
        update_fields: Optional[Iterable[str]] = None,
        force_create: bool = False,
        force_update: bool = False,
    ):
        self.deleted_at = datetime.now()
        self.deleted_by = current_user()

        await self.save(using_db, update_fields, force_create, force_update)


class Router:

    def db_for_read(self, model: Type[TortoiseModel]):
        # return "readonly"
        return "default"

    def db_for_write(self, model: Type[TortoiseModel]):
        # return "primary"
        return "default"


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

    setattr(cls, "as_form", as_form_func)

    return cls
