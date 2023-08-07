import json
from uuid import UUID

from app.src.database import Base

from .conn import client

# from fastapi.encoders import jsonable_encoder


DISH_PRICE_ENCODER = {float: lambda x: f'{round(float(x), 2):.2f}'}


async def cache_set(key: UUID | str, value: Base) -> None:
    # data = jsonable_encoder(value.__dict__, custom_encoder=DISH_PRICE_ENCODER)
    # await client.set(str(key), json.dumps(data))
    return


async def cache_get(key: UUID | str) -> dict | None:
    data = await client.get(str(key))
    if data:
        return json.loads(data)
    return None


async def cache_del(key: UUID | str) -> None:
    await client.delete(str(key))
    return
