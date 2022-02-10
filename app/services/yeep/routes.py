import logging
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from services.yeep import models
from services import BaseSerializer



logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/yeeps",
    tags=["yeeps"],
    dependencies=[],
)


class YeepCreateRequest(BaseModel):
    sign: str


class YeepTactCreateRequest(BaseModel):
    tact_id: str


class Serializer(BaseSerializer):
    data: list[models.YeepData]


class SerializerYeepTact(BaseSerializer):
    data: list[models.YeepTactData]


@router.get("/", response_model=Serializer)
async def yeeps(yeep_id: Optional[str] = None):
    data = await models.yeeps(yeep_id=yeep_id)
    return Serializer(data=data)


@router.post("/", response_model=Serializer)
async def create_yeep(item: YeepCreateRequest):
    data = await models.create_yeep(sign=item.sign)
    return Serializer(data=[data])


@router.get("/{yeep_id}/tacts", response_model=SerializerYeepTact)
async def yeep_tacts(yeep_id: str, tact_id: Optional[str] = None):
    data = await models.yeep_tacts(yeep_id=yeep_id, tact_id=tact_id)
    return SerializerYeepTact(data=data)


@router.post("/{yeep_id}/tacts", response_model=SerializerYeepTact)
async def create_yeep_tact(yeep_id: str, item: YeepTactCreateRequest):
    data = await models.create_yeep_tact(
        yeep_id=yeep_id,
        tact_id=item.tact_id,
    )
    return SerializerYeepTact(data=[data])
