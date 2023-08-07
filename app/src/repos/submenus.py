from uuid import UUID

from fastapi import Depends, HTTPException

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import schemas
from app.src.crud import CRUDSubMenus
from app.src.database import get_db

from .base import BaseRepository
from .menus import MenuRepository


class SubMenuRepository(BaseRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        super().__init__(CRUDSubMenus(), db)

    async def get_by_menu(self, menu_id: UUID):
        return await CRUDSubMenus().get_by_menu(menu_id, self.db)

    async def create_submenu(self, obj: schemas.CreateSubMenu):
        assert obj.menu_id
        if not (await MenuRepository(self.db).get(obj.menu_id)):
            raise HTTPException(status_code=404, detail='menu not found')

        return await self.create(obj)

    async def update_submenu(self):
        # TODO забрать функционал с сервисного слоя (там проверки на существование меню)
        pass

    async def delete_submenu(self):
        # TODO забрать функционал с сервисного слоя (там проверки на существование меню)
        pass
