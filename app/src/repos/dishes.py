from uuid import UUID

from fastapi import Depends, HTTPException

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import schemas
from app.src.crud import CRUDDishes, CRUDMenus, CRUDSubMenus
from app.src.database import get_db

from .base import BaseRepository


class DishesRepository(BaseRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        super().__init__(CRUDDishes(), db)

    async def get_by_submenu(self, menu_id: UUID, submenu_id: UUID):
        db_submenu = await CRUDSubMenus().get(submenu_id, self.db)
        if not db_submenu or db_submenu.menu_id != menu_id:
            return []
        return await CRUDDishes().get_by_submenu(submenu_id, self.db)

    async def get_by_ids_path(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
        # TODO подумать. используя crud не попадаем в кэш (
        db_submenu = await CRUDSubMenus().get(submenu_id, self.db)
        if not db_submenu or db_submenu.menu_id != menu_id:
            raise HTTPException(status_code=404, detail='submenu not found')

        db_dish = await self.crud.get(dish_id, self.db)
        if not db_dish or db_dish.submenu_id != submenu_id:
            raise HTTPException(status_code=404, detail='dish not found')

        return db_dish

    async def create_with_menu(self, menu_id: UUID, obj: schemas.CreateDish):
        # TODO убрать menu_id куда-то (((
        # check the menu exists
        if not (await CRUDMenus().get(menu_id, self.db)):
            raise HTTPException(status_code=404, detail='menu not found')
        # check the submenu exists
        assert obj.submenu_id
        db_submenus = await CRUDSubMenus().get(obj.submenu_id, self.db)
        if not db_submenus or db_submenus.menu_id != menu_id:
            raise HTTPException(status_code=404, detail='submenu not found')

        return await self.create(obj)
