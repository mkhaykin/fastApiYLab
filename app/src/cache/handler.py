from uuid import UUID

from fastapi import Depends

from app.src.schemas import BaseSchema, TBaseSchema

from .cache import Cache, get_cache


class CacheHandler:
    def __init__(self, cache=Depends(get_cache)):
        self._cache: Cache = cache

    @staticmethod
    def _key(
            scope: str | None = None,
            menu_id: UUID | None = None,
            submenu_id: UUID | None = None,
            dish_id: UUID | None = None,
    ) -> str:
        return f'{scope}:{menu_id}:{submenu_id}:{dish_id}'

    async def add(
            self, /,
            scope: str | None = None,
            menu_id: UUID | None = None,
            submenu_id: UUID | None = None,
            dish_id: UUID | None = None,
            data: list[TBaseSchema] | TBaseSchema | None = None,
    ):
        key = self._key(scope, menu_id, submenu_id, dish_id)
        await self._cache.set(key, data)

    def linked_keys(
            self, /,
            scope: str | None = '*',
            menu_id: UUID | None = None,
            submenu_id: UUID | None = None,
            dish_id: UUID | None = None,
    ) -> list[str]:
        result = [self._key(scope, menu_id, submenu_id, dish_id)]
        if dish_id:
            result.extend((
                f'{scope}:{menu_id}:{submenu_id}:{dish_id}',
                f'{scope}:{menu_id}:{submenu_id}:None',
                f'{scope}:{menu_id}:None:None',
                f'{scope}:None:None:None',
            ))
        if submenu_id:
            result.extend((
                f'{scope}:{menu_id}:{submenu_id}:*',
                f'{scope}:{menu_id}:None:None',
                f'{scope}:None:None:None',
            ))
        if menu_id:
            result.extend((
                f'{scope}:{menu_id}:*:*',
                f'{scope}:None:None:None',
            ))
        return result

    async def delete(
            self, /,
            scope: str | None = None,
            menu_id: UUID | None = None,
            submenu_id: UUID | None = None,
            dish_id: UUID | None = None,
    ) -> None:
        linked_keys = self.linked_keys(scope, menu_id, submenu_id, dish_id)
        for key in linked_keys:
            await self._cache.delete_pattern(key)

    async def get(
            self, /,
            scope: str | None = None,
            menu_id: UUID | None = None,
            submenu_id: UUID | None = None,
            dish_id: UUID | None = None,
    ) -> list[TBaseSchema] | TBaseSchema | None:
        key = self._key(scope, menu_id, submenu_id, dish_id)
        cache: list[BaseSchema] | None = await self._cache.get(key)
        if cache:
            return cache
        return None
