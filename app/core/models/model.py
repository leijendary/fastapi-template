from datetime import datetime
from inspect import Parameter, signature
from typing import Iterable, Optional, Type, Any

from fastapi import Form
from fastapi_pagination import create_page
from pydantic import BaseModel
from pydantic.fields import ModelField
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.expressions import Q
from tortoise.fields import DatetimeField
from tortoise.fields.data import TextField, BigIntField
from tortoise.models import Model as TortoiseModel
from tortoise.queryset import QuerySet

from app.core.constants import CONNECTION_PRIMARY, CONNECTION_READONLY
from app.core.context.request_context import current_user
from app.core.data.params import SortParams, SeekParams
from app.core.data.seek import Seek, SeekToken
from app.core.utils.dict_util import to_dict

_SEEK_SORT_FIELDS = ["-created_at", "-row_id"]


class Model(TortoiseModel):
    class Meta:
        abstract = True

    def dict(self):
        return to_dict(self)

    def kafka_dict(self):
        return self.dict()


class SeekableMixin(Model):
    row_id = BigIntField(generated=True, null=False)
    created_at = DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True


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
    def db_for_write(self, model: Type[TortoiseModel]):
        return CONNECTION_PRIMARY

    def db_for_read(self, model: Type[TortoiseModel]):
        return CONNECTION_READONLY


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


async def to_page(query: QuerySet[Model], params: SortParams, cls: Any):
    raw_params = params.to_raw_params()
    items = await (
        query
            .offset(raw_params.offset)
            .limit(raw_params.limit)
            .order_by(*params.sort.split(","))
            .all()
    )
    total = await query.count()
    records = [cls(**item.dict()) for item in items]

    return create_page(records, total, params)


async def to_seek(
        query: QuerySet[SeekableMixin],
        params: SeekParams,
        cls: Any
) -> Seek[Any]:
    next_token = params.next_token
    limit = params.limit

    if next_token:
        seek_token = SeekToken.from_token(next_token)
        created_at = seek_token.created_at
        row_id = seek_token.row_id

        q = Q(
            Q(created_at__lt=created_at),
            Q(Q(created_at=created_at), Q(row_id__lt=row_id)),
            join_type=Q.OR
        )

        query = query.filter(q)

        # Clear the next token
        next_token = None

    items = (
        await query
            .order_by(*_SEEK_SORT_FIELDS)
            .limit(limit + 1)
            .all()
    )
    size = len(items)

    if size > limit:
        items = items[:limit]
        last = items[-1]
        size = size - 1
        seek_token = SeekToken(last.created_at, last.row_id)
        next_token = seek_token.next_token()

    content = [cls(**item.dict()) for item in items]

    return Seek.create(content, next_token, size, limit)
