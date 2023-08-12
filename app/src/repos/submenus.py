from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import crud, schemas
from app.src.cache import Cache, get_cache
from app.src.database import get_db

from .base import BaseRepository
from .menus import MenuRepository


class SubMenuRepository(BaseRepository):
    _crud: crud.SubMenusCRUD
    _name: str = 'submenu'

    def __init__(self, session: AsyncSession = Depends(get_db), cache: Cache = Depends(get_cache)):
        super().__init__(session, cache)
        self._crud = crud.SubMenusCRUD(session)

    async def check(self, menu_id: UUID):
        if not (await MenuRepository(self._session, self._cache).get_by_ids(menu_id)):
            raise HTTPException(status_code=404, detail='menu not found')

    async def get_by_ids(self, menu_id: UUID, submenu_id: UUID | None = None) -> list[schemas.GetSubMenu]:
        if self._cache:
            cache: list[schemas.BaseSchema] | None
            cache = await self._cache.cache_get(f"{menu_id}:{submenu_id if submenu_id else 'submenu'}:None")
            if cache:
                return cache

        items = await crud.SubMenusCRUD(self._session).get_by_ids(menu_id, submenu_id)
        result = [schemas.GetSubMenu(**item) for item in items]

        await self._cache.cache_set(f"{menu_id}:{submenu_id if submenu_id else 'submenu'}:None", result)
        return result

    async def create_submenu(self, menu_id: UUID, menu: schemas.CreateSubMenuIn) -> schemas.CreateSubMenuOut:
        await self.check(menu_id)
        if self._cache:
            await self._cache.cache_del_pattern(f'{menu_id}:*:*')
        return schemas.CreateSubMenuOut(**await self._create(**{'menu_id': menu_id, **menu.model_dump()}))

    async def update_submenu(self, menu_id: UUID, submenu_id: UUID,
                             submenu: schemas.UpdateSubMenuIn) -> schemas.UpdateSubMenuOut:
        if self._cache:
            await self._cache.cache_del_pattern(f'*:{submenu_id}:*')
        await self.check(menu_id)
        return schemas.UpdateSubMenuOut(**await self._update(submenu_id, **submenu.model_dump()))

    async def delete_submenu(self, menu_id: UUID, submenu_id: UUID):
        await self.check(menu_id)
        if self._cache:
            await self._cache.cache_del_pattern(f'{menu_id}:*:*')
        await self._delete(submenu_id)
