from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import crud, schemas
from app.src.cache import CacheSubMenusHandler
from app.src.cache.cache import Cache
from app.src.database import get_db

from .base import BaseRepository
from .menus import MenuRepository


class SubMenuRepository(BaseRepository):
    _crud: crud.SubMenusCRUD
    _name: str = 'submenu'

    def __init__(
            self,
            session: AsyncSession = Depends(get_db),
            cache_handler: CacheSubMenusHandler = Depends(),
            menu_repo: MenuRepository = Depends(),
    ):
        super().__init__(session, Cache())
        self._crud = crud.SubMenusCRUD(session)
        self._cache_handler = cache_handler
        self._menu_repo = menu_repo

    async def check(
            self,
            menu_id: UUID
    ):
        if not (await self._menu_repo.get_by_ids(menu_id)):
            raise HTTPException(status_code=404, detail='menu not found')

    async def get_by_ids(
            self,
            menu_id: UUID,
            submenu_id: UUID | None = None
    ) -> list[schemas.GetSubMenu]:
        cache: list[schemas.GetSubMenu] | None
        cache = await self._cache_handler.get(menu_id, submenu_id)
        if cache:
            return cache
        # if self._cache:
        #     cache: list[schemas.BaseSchema] | None
        #     cache = await self._cache.cache_get(f"{menu_id}:{submenu_id if submenu_id else 'submenu'}:None")
        #     if cache:
        #         return cache

        items = await crud.SubMenusCRUD(self._session).get_by_ids(menu_id, submenu_id)
        result = [schemas.GetSubMenu(**item) for item in items]

        # await self._cache.cache_set(f"{menu_id}:{submenu_id if submenu_id else 'submenu'}:None", result)
        await self._cache_handler.add(menu_id, submenu_id, result)
        return result

    async def create_submenu(
            self,
            menu_id: UUID,
            menu: schemas.CreateSubMenuIn,
            obj_id: UUID | None = None,
    ) -> schemas.CreateSubMenuOut:
        await self.check(menu_id)
        return schemas.CreateSubMenuOut(**await self._create(**{'menu_id': menu_id, **menu.model_dump(), 'id': obj_id}))

    async def update_submenu(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            submenu: schemas.UpdateSubMenuIn
    ) -> schemas.UpdateSubMenuOut:
        await self.check(menu_id)
        return schemas.UpdateSubMenuOut(**await self._update(submenu_id, **submenu.model_dump()))

    async def delete_submenu(
            self,
            menu_id: UUID,
            submenu_id: UUID
    ):
        await self.check(menu_id)
        await self._delete(submenu_id)
