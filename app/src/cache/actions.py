import json
from typing import TypeVar
from uuid import UUID

from fastapi.encoders import jsonable_encoder

from app.src.models.base import Base
from app.src.schemas.dish import DISH_PRICE_ENCODER

from .conn import client

T = TypeVar('T', bound=Base)


async def cache_reset() -> None:
    await client.flushall(asynchronous=True)
    return


async def cache_set(key: UUID | str, name: str, value: T) -> None:
    data = jsonable_encoder(value.__dict__, custom_encoder=DISH_PRICE_ENCODER)
    await client.set(name + str(key), json.dumps(data), ex=30)
    return


async def cache_get(key: UUID | str, name: str) -> dict | None:
    # data = await client.get(name + str(key))
    data = None
    if data:
        return json.loads(data)
    return None


async def cache_del(key: UUID | str, name: str) -> None:
    await client.delete(name + str(key))
    return
