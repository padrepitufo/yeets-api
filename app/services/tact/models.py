import logging
from typing import Optional

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from utils import (
    uuid,
    date,
)


logger = logging.getLogger(__name__)



async def tact_listing(tact_id: str):
    # TODO filters
    return await TactData.from_queryset(Tact.all())


async def tact_create(tact_type_id: str, args: str):
    tact_type = await TactType.get(id=tact_type_id)
    tact_id = uuid.generate()
    await Tact.create(
        id=tact_id,
        type=tact_type,
        args=args,
    )
    return await TactData.from_queryset_single(Tact.get(id=tact_id))


async def tact_type_listing(tact_type_id: str):
    # TODO filters
    logger.error(f"got tact type id: {tact_type_id}")
    return await TactTypeData.from_queryset(TactType.all())


async def tact_type_create(name: str, params: str, tact_type_id: Optional[str] = None):
    # TODO idempotent this so it doens't fail on duplicate attempts
    tact_type_id = tact_type_id or uuid.generate()
    await TactType.create(
        id=tact_type_id,
        name=name,
        params=params,
    )
    return await TactTypeData.from_queryset_single(TactType.get(id=tact_type_id))


async def tact_confirmation_request_listing(tact_id: str):
    # TODO filters
    return await TactConfirmationRequestData.from_queryset(TactConfirmationRequest.all())


async def tact_confirmation_request_create(tact_id: str):
    tact = await Tact.get(id=tact_id)
    request_id = uuid.generate()
    await TactConfirmationRequest.create(
        id=request_id,
        tact=tact,
        expired_at=None,  # MAKE TO A DATE
    )
    return await TactConfirmationRequestData.from_queryset_single(TactConfirmationRequest.get(id=request_id))


async def tact_confirmation_listing(request_id:str):
    # TODO filters
    return await TactConfirmationData.from_queryset(TactConfirmation.all())


async def tact_confirmation_create(request_id: str, meta_data: str):
    signed_at = date.now()
    confirmation_request = await TactConfirmationRequest.get(id=request_id)
    tact_confirmation_id = uuid.generate()
    await TactConfirmation.create(
        id=tact_confirmation_id,
        meta_data=meta_data,  # get metadata
        request=confirmation_request,
        signed_at=signed_at,  # MAKE TO A DATE
    )
    return await TactConfirmationData.from_queryset_single(TactConfirmation.get(id=tact_confirmation_id))


class TactType(Model):
    id = fields.UUIDField(pk=True, default=None)
    name = fields.CharField(max_length=36, unique=True)
    params = fields.CharField(max_length=1024)


class Tact(Model):
    id = fields.UUIDField(pk=True, default=None)
    type: fields.ForeignKeyNullableRelation[TactType] = fields.ForeignKeyField(
        "app.TactType",
        on_delete=fields.SET_NULL,
        null=True,
    )
    args = fields.CharField(max_length=2048, unique=True)


class TactConfirmationRequest(Model):
    id = fields.UUIDField(pk=True, default=None)
    tact: fields.ForeignKeyNullableRelation[Tact] = fields.ForeignKeyField(
        "app.Tact",
        on_delete=fields.SET_NULL,
        null=True,
    )
    expired_at = fields.DateField(null=True)


class TactConfirmation(Model):
    id = fields.UUIDField(pk=True, default=None)
    request: fields.ForeignKeyNullableRelation[TactConfirmationRequest] = fields.ForeignKeyField(
        "app.TactConfirmationRequest",
        on_delete=fields.SET_NULL,
        null=True,
    ) # should be unique?
    signed_at = fields.DateField(null=False)
    meta_data = fields.CharField(max_length=2048, null=True)


TactData = pydantic_model_creator(Tact, name="Tact", include=("id", "type", "args"))
TactConfirmationRequestData = pydantic_model_creator(TactConfirmationRequest, name="TactConfirmationRequest", include=("id", "tact", "expired_at"))
TactConfirmationData = pydantic_model_creator(TactConfirmation, name="TactConfirmation", include=("id", "request", "signed_at", "meta_data"))
TactTypeData = pydantic_model_creator(TactType, name="TactType", include=("id", "name", "params"))