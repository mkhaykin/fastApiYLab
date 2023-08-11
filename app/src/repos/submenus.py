from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import crud, schemas
from app.src.cache.actions import cache_del
from app.src.database import get_db

from .base import BaseRepository
from .menus import MenuRepository


class SubMenuRepository(BaseRepository):
    _crud: crud.SubMenusCRUD

    def __init__(self, session: AsyncSession = Depends(get_db)):
        super().__init__(session)
        self._crud = crud.SubMenusCRUD(session)

    async def get_by_ids(self, menu_id: UUID, submenu_id: UUID | None = None) -> list[schemas.GetSubMenu]:
        items = await crud.SubMenusCRUD(self._session).get_by_ids(menu_id, submenu_id)
        return [schemas.GetSubMenu(**item) for item in items]

    async def create_submenu(self, menu_id: UUID, menu: schemas.CreateSubMenuIn) -> schemas.CreateSubMenuOut:
        # check menu exists
        if not (await MenuRepository(self._session).get(menu_id)):
            raise HTTPException(status_code=404, detail='menu not found')

        await cache_del(menu_id, 'menu')
        return schemas.CreateSubMenuOut(**await self._create(**{'menu_id': menu_id, **menu.model_dump()}))

    async def update_submenu(self, menu_id: UUID, submenu_id: UUID,
                             submenu: schemas.UpdateSubMenuIn) -> schemas.UpdateSubMenuOut:
        if not (await MenuRepository(self._session).get(menu_id)):
            raise HTTPException(404, 'menu not found')

        return schemas.UpdateSubMenuOut(**await self._update(submenu_id, **submenu.model_dump()))

    async def delete_submenu(self, menu_id: UUID, submenu_id: UUID):
        # check menu exists
        if not (await MenuRepository(self._session).get(menu_id)):
            raise HTTPException(404, 'menu not found')

        await self._delete(submenu_id)
        await cache_del(menu_id, 'menu')
