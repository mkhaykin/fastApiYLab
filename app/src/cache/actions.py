"""
    Функции для тестирования с использованием кеша
"""
from typing import TypeVar

from app.src.models.base import Base

from .conn import client

T = TypeVar('T', bound=Base)


async def cache_reset() -> None:
    return await client.flushall(asynchronous=True)


async def key_pattern_in_cache(pattern: str) -> bool:
    for key in await client.keys(pattern):
        if await client.exists(key):
            return True
    return False


async def key_in_cache(key: str) -> bool:
    return await client.exists(key)
