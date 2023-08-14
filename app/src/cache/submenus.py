from uuid import UUID

from app.src.schemas import BaseSchema

from .cache import Cache


class CacheSubMenusHandler:
    def __init__(self):
        self._cache = Cache()

    @staticmethod
    def key(menu_id: UUID, submenu_id: UUID | None):
        return f"{menu_id}:{str(submenu_id) if submenu_id else 'submenus'}:None"

    async def add(self, menu_id: UUID, submenu_id: UUID | None, data: list[BaseSchema]):
        await self._cache.cache_set(self.key(menu_id, submenu_id), data)

    async def delete(self, menu_id: UUID, submenu_id: UUID | None) -> None:
        # TODO think
        await self._cache.cache_del(f'{menu_id}:{submenu_id}:None')
        await self._cache.cache_del(f'{menu_id}:full:None')
        await self._cache.cache_del(f'{menu_id}:None:None')
        # OR
        await self._cache.cache_del_pattern(f'{menu_id}:*:*')
        await self._cache.cache_del('menus:*:*')
        await self._cache.cache_del('full:*:*')

    async def get(self, menu_id: UUID, submenu_id: UUID | None) -> list[BaseSchema] | None:
        cache = await self._cache.cache_get(self.key(menu_id, submenu_id))
        if cache:
            return cache
        return None
