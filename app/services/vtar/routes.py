import logging
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from services.star import models
from services import BaseSerializer

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/vtars",
    tags=["vtars"],
    dependencies=[],
)

class Validator(BaseModel):
    yeep_id: str
    url: str


class Serializer(BaseSerializer):
    data: list[models.StarData]


@router.get("/", response_model=Serializer)
async def listing(yeet_id: Optional[str] = None):
    data = await models.listing(vtar_id=vtar_id)
    return Serializer(data=data)


@router.delete("/{vtar_id}", response_model=Serializer)
async def remove(vtar_id: str):
    try:
        data = await models.remove(vtar_id=vtar_id)
    except RuntimeError as e:
        return Serializer(data=[], message=str(e), success=False)
    return Serializer(data=data)


@router.post("/", response_model=Serializer)
async def add(item: Validator):
    try:
        data = await models.add(
            yeep_id=item.yeep_id,
            url=item.url,
        )
    except RuntimeError as e:
        return Serializer(data=[], message=str(e), success=False)
    return Serializer(data=data)