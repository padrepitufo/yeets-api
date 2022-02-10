from typing import Optional

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from services.tact.models import Tact
from utils import uuid



async def yeeps(yeep_id: str):
    filters = {}
    if yeep_id:
        filters.update(id=yeep_id)
    return await YeepData.from_queryset(Yeep.filter(**filters).all())


async def create_yeep(sign):
    # TODO check if sign taken (which means that the sign has a tact associated)
    yeep_id = uuid.generate()
    await Yeep.create(id=yeep_id, sign=sign)
    return await YeepData.from_queryset_single(Yeep.get(id=yeep_id))


async def yeep_tacts(yeep_id: Optional[str], tact_id: Optional[str]):
    filters = {}
    
    if yeep_id:
        filters.update(yeep_id=yeep_id)
    
    if tact_id:
        filters.update(tact_id=tact_id)

    return await YeepTactData.from_queryset(YeepTact.filter(**filters).all())


async def create_yeep_tact(yeep_id: str, tact_id: str):
    tact = await Tact.get(id=tact_id)
    yeep = await Yeep.get(id=yeep_id)
    yeep_tact_id = uuid.generate()
    await YeepTact.create(id=yeep_tact_id, yeep=yeep, tact=tact)
    return await YeepTactData.from_queryset_single(YeepTact.get(id=yeep_tact_id))


class Yeep(Model):
    id = fields.UUIDField(pk=True, default=None)
    sign = fields.CharField(max_length=2048, unique=True)


class YeepTact(Model):
    id = fields.UUIDField(pk=True, default=None)
    yeep: fields.ForeignKeyNullableRelation[Yeep] = fields.ForeignKeyField(
        "app.Yeep",
        on_delete=fields.SET_NULL,
        null=True,
    )
    tact: fields.ForeignKeyNullableRelation[Tact] = fields.ForeignKeyField(
        "app.Tact",
        on_delete=fields.SET_NULL,
        null=True,
    )
    
    class Meta:
        unique_together = ("yeep", "tact")
    


YeepData = pydantic_model_creator(Yeep, name="Yeep", include=("id", "sign"))
YeepTactData = pydantic_model_creator(Yeep, name="YeepTact", include=("id", "yeep", "tact"))