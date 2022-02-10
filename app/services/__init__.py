from pydantic import BaseModel

from services.yeet.models import Yeet


async def initialize():
    is_populated = await _is_populated()
    if is_populated:
        return
    # TODO populate the tables


async def _is_populated() -> bool:
    """quick test to see if any table exists"""
    try:
        await Yeet.get(id=1)
        return True
    except:  # noqa E722
        return False


class BaseSerializer(BaseModel):
    data: list = []
    message: str = ""
    success: bool = True
