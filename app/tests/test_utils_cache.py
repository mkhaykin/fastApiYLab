"""
    Функции для тестирования с использованием кеша
"""
from typing import TypeVar

import aioredis
from aioredis.client import Redis

from app.src.config import settings
from app.src.models.base import Base

T = TypeVar('T', bound=Base)
REDIS_URL: str = f'redis://{settings.REDIS_SERVER}:{settings.REDIS_PORT}'
client: Redis = aioredis.from_url(REDIS_URL)


async def cache_reset() -> None:
    return await client.flushall(asynchronous=True)


async def key_pattern_in_cache(pattern: str) -> bool:
    for key in await client.keys(pattern):
        if await client.exists(key):
            return True
    return False


async def key_in_cache(key: str) -> bool:
    return await client.exists(key)


async def keys_in_cache() -> list[str]:
    return [str(key) for key in (await client.keys('*'))]
