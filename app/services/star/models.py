import logging
from typing import Optional

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from services.yeep.models import Yeep
from services.yeet.models import Yeet

logger = logging.getLogger(__name__)


async def listing(yeet_id: Optional[str]):
    filters = {}
    if yeet_id is not None:
        filters.update(yeet_id=yeet_id)
    return await StarData.from_queryset(Star.filter(**filters).all())

async def increment(yeet_id: str, giver_id: str) -> list["Star"]:
    await _add_rating(yeet_id=yeet_id, giver_id=giver_id, rating=1)
    return await _get_stars(yeet_id=yeet_id)


async def decrement(yeet_id, giver_id) -> list["Star"]:
    await _add_rating(yeet_id=yeet_id, giver_id=giver_id, rating=-1)
    return await _get_stars(yeet_id=yeet_id)


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


class Star(Model):
    id = fields.IntField(pk=True)
    yeet: fields.ForeignKeyNullableRelation[Yeet] = fields.ForeignKeyField(
        "app.Yeet",
        on_delete=fields.SET_NULL,
        null=True,
    )
    giver: fields.ForeignKeyNullableRelation[Yeep] = fields.ForeignKeyField(
        "app.Yeep",
        on_delete=fields.SET_NULL,
        null=True,
    )
    rating = fields.SmallIntField()


StarData = pydantic_model_creator(Star, name="Star", include=("id", "yeet", "giver_id", "rating"))