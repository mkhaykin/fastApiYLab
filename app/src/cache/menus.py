from uuid import UUID

from app.src.schemas import BaseSchema

from .cache import Cache


class CacheMenusHandler:
    def __init__(self):
        self._cache = Cache()

    @staticmethod
    def key(menu_id: UUID | None):
        return (str(menu_id) if menu_id else 'menus') + ':None:None'

    async def add(self, menu_id: UUID | None, data: list[BaseSchema]):
        await self._cache.set(self.key(menu_id), data)

    async def delete(self, menu_id: UUID | None) -> None:
        await self._cache.delete('menus:None:None')
        await self._cache.delete('full:None:None')
        await self._cache.delete_pattern(f'{menu_id}:*:*')

    async def get(self, menu_id: UUID | None) -> list[BaseSchema] | None:
        cache = await self._cache.get(self.key(menu_id))
        if cache:
            return cache
        return None
