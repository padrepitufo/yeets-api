import logging
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from services.star import models
from services import BaseSerializer

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/stars",
    tags=["stars"],
    dependencies=[],
)

class Validator(BaseModel):
    yeep_id: str


class Serializer(BaseSerializer):
    data: list[models.StarData]


@router.get("/", response_model=Serializer)
async def stars(yeet_id: Optional[str] = None):
    data = await models.listing(yeet_id=yeet_id)
    return Serializer(data=data)


@router.post("/yeet/{yeet_id}/booooooo", response_model=Serializer)
async def stars_decrement(yeet_id: str, item: Validator):
    data = await models.decrement(yeet_id=yeet_id, giver_id=item.yeep_id)
    return Serializer(data=data)


@router.post("/yeet/{yeet_id}/yaaaaaay", response_model=Serializer)
async def stars_increment(yeet_id: str, item: Validator):
    data = await models.increment(yeet_id=yeet_id, giver_id=item.yeep_id)
    return Serializer(data=data)