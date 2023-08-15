from uuid import UUID

from fastapi import Depends

from app.src.schemas import BaseSchema

from .cache import Cache, get_cache


class CacheSubMenusHandler:
    def __init__(self, cache=Depends(get_cache)):
        self._cache: Cache = cache

    @staticmethod
    def key(menu_id: UUID, submenu_id: UUID | None):
        return f"{menu_id}:{str(submenu_id) if submenu_id else 'submenus'}:None"

    async def add(self, menu_id: UUID, submenu_id: UUID | None, data: list[BaseSchema]):
        await self._cache.set(self.key(menu_id, submenu_id), data)

    async def delete(self, menu_id: UUID, submenu_id: UUID | None) -> None:
        # TODO think
        await self._cache.delete(f'{menu_id}:{submenu_id}:None')
        await self._cache.delete(f'{menu_id}:full:None')
        await self._cache.delete(f'{menu_id}:None:None')
        # OR
        await self._cache.delete_pattern(f'{menu_id}:*:*')
        await self._cache.delete('menus:*:*')
        await self._cache.delete('full:*:*')

    async def get(self, menu_id: UUID, submenu_id: UUID | None) -> list[BaseSchema] | None:
        return await self._cache.get(self.key(menu_id, submenu_id))
