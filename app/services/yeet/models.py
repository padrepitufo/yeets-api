from typing import Optional

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from services.yeep.models import Yeep
from utils import uuid


async def listing(yeet_id: Optional[str] = None, yeep_id: Optional[str] = None):
    filters = {}

    if yeep_id:
        filters.update(creator=yeep_id)
    
    if yeet_id:
        filters.update(id=yeet_id)
    
    return await YeetData.from_queryset(Yeet.filter(**filters).all())


async def create(yeep_id: str, content: str, title: str, snippet: str, slug: str):
    creator = await Yeep.get(id=yeep_id)
    yeet_id = uuid.generate()
    await Yeet.create(
        id=yeet_id,
        content=content,
        creator=creator,
        title=title,
        snippet=snippet,
        slug=slug
    )
    return await YeetData.from_queryset_single(Yeet.get(id=yeet_id))


class Yeet(Model):
    id = fields.UUIDField(pk=True, default=None)
    creator: fields.ForeignKeyNullableRelation[Yeep] = fields.ForeignKeyField(
        "app.Yeep",
        on_delete=fields.SET_NULL,
        null=True,
    )
    content = fields.CharField(max_length=2048)
    title = fields.CharField(max_length=70)
    snippet = fields.CharField(max_length=280)
    slug = fields.CharField(max_length=140, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)


YeetData = pydantic_model_creator(Yeet, name="Yeet", include=("id", "creator", "created_at", "content", "title", "snippet", "slug"))