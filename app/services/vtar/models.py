import logging
from typing import Optional

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from services.yeep.models import Yeep
from services.yeet.models import Yeet

logger = logging.getLogger(__name__)


async def listing(vtar_id: Optional[str]):
    filters = {}
    if vtar_id is not None:
        filters.update(vtar_id=vtar_id)
    return await StarData.from_queryset(Star.filter(**filters).all())

async def remove(vtar_id):
    pass


async def add(yeep_id: str, url: str):
    pass




async def _add_rating(yeet_id, giver_id, rating):
    yeet = await Yeet.get(id=yeet_id)
    yeep = await Yeep.get(id=giver_id)

    exists = await Star.filter(giver=yeep, yeet=yeet).first()
    if exists:
        raise RuntimeError(f"yeeter {yeep.sign} has already opined on {yeet.title}")

    await Star.create(
        yeet=yeet,
        giver=yeep,
        rating=rating,
    )


async def _get_stars(yeet_id) -> list["Star"]:
    stars = await StarData.from_queryset(Star.filter(yeet_id=yeet_id).all())
    logging.debug(stars)
    return stars


class Vtar(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=2048, unique=True)
    added_by: fields.ForeignKeyNullableRelation[Yeep] = fields.ForeignKeyField(
        "app.Yeep",
        on_delete=fields.SET_NULL,
        null=True,
    )


VtarData = pydantic_model_creator(Vtar, name="Vtar", include=("id", "url", "added_by"))