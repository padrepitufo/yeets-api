from typing import Union

from tortoise import Tortoise

from utils import config

DATABASE_URL = config.DATABASE_URL


async def initialize():
    await Tortoise.generate_schemas()


async def start():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={
            "app": [
                "services.star.models",
                "services.tact.models",
                "services.yeep.models",
                "services.yeet.models",
            ]
        },
    )
    await Tortoise.generate_schemas()


async def stop():
    await Tortoise.close_connections()


async def raw(sql: str, values: Union[list[list], list]):
    await Tortoise.get_connection("default").execute_query(sql, _flatten(values))


def _flatten(collection: Union[list[list], list]) -> list:
    already_flat = collection and not isinstance(collection[0], list)
    if already_flat:
        return collection
    return [sub_item for sub_collection in collection for sub_item in sub_collection]