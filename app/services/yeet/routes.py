import logging
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from services.yeet import models
from services import BaseSerializer

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/yeets",
    tags=["yeets"],
    dependencies=[],
)

class CreateValidator(BaseModel):
    content: str
    title: str
    snippet: str
    slug: str
    yeep_id: str

class Serializer(BaseSerializer):
    data: list[models.YeetData]


@router.get("/", response_model=Serializer)
async def yeets(yeet_id: Optional[str] = None):
    data = await models.listing(yeet_id=yeet_id)
    return Serializer(data=data)


@router.post("/", response_model=Serializer)
async def create_yeet(item: CreateValidator):
    data = await models.create(
        content=item.content,
        snippet=item.snippet,
        slug=item.slug,
        title=item.title,
        yeep_id=item.yeep_id,
    )
    return Serializer(data=[data])
