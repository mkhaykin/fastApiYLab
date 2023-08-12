import pickle
from uuid import UUID

import aioredis
from aioredis.client import Redis

from app.src import schemas

from .conn import REDIS_URL


class Cache:
    __instance = None

    def __new__(cls):
        if not isinstance(cls.__instance, cls):
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        # if not Cache.__instance:
        self.client: Redis = aioredis.from_url(REDIS_URL)

    async def reset(self) -> None:
        await self.client.flushall(asynchronous=True)

    async def cache_set(self, key: UUID | str, data: list[schemas.TBaseSchema]) -> None:
        print('set cache')
        byte_data = pickle.dumps(data)
        await self.client.set(str(key), byte_data, ex=30)
        return

    async def cache_get(self, key: UUID | str) -> list[schemas.TBaseSchema] | None:
        print('get cache')
        data = await self.client.get(str(key))
        if not data:
            return None
        data = pickle.loads(data)
        return data

    async def cache_del_pattern(self, pattern: str) -> None:
        print('del cache pattern')
        for key in await (self.client.keys(pattern)):
            await self.client.delete(key)
        return

    async def cache_del(self, key: UUID | str) -> None:
        print('del cache')
        await self.client.delete(str(key))
        return

    def __str__(self):
        return 'redis cache'


cache = Cache()


async def get_cache():
    # cache = Cache()
    yield cache
