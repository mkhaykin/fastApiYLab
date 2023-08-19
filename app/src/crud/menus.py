from typing import Sequence
from uuid import UUID

from fastapi import Depends
from sqlalchemy import RowMapping, String, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import models
from app.src.database import get_db

from .base import BaseCRUD


class MenusCRUD(BaseCRUD):
    _model = models.Menus
    _name_for_error = 'menu'

    def __init__(self, session: AsyncSession = Depends(get_db)):
        super().__init__(session)
        self._model = models.Menus
        self._base_select = (
            select(
                models.Menus.id,
                models.Menus.title,
                models.Menus.description,
                func.count(distinct(models.SubMenus.id)).label('submenus_count'),
                func.count(distinct(models.Dishes.id)).label('dishes_count'),
            )
            .outerjoin(models.SubMenus, models.Menus.id == models.SubMenus.menu_id)
            .outerjoin(models.Dishes, models.SubMenus.id == models.Dishes.submenu_id)
            .group_by(models.Menus.id)
        )

    async def get_by_ids(self, menu_id: UUID | None = None) -> Sequence[RowMapping]:
        query = (
            self.base_select)
        if menu_id:
            query = query.where(self.model.id == menu_id)
        db_menus = (await self._session.execute(query))
        return db_menus.mappings().all()

    async def get_orm_all(self):
        submenus_count = (
            select(
                models.SubMenus.menu_id,
                func.count(models.SubMenus.id).label('submenus_count'),
            )
            .group_by(models.SubMenus.menu_id)
            .subquery()
        )

        dishes_count = (
            select(
                models.SubMenus.menu_id,
                func.count(models.Dishes.id).label('dishes_count'),
            )
            .outerjoin(models.Dishes, models.Dishes.submenu_id == models.SubMenus.id)
            .group_by(models.SubMenus.menu_id)
            .subquery()
        )

        dishes_in_submenu_count = (
            select(
                models.SubMenus.id,
                func.count(models.Dishes.id).label('dishes_in_submenu_count'),
            )
            .outerjoin(models.Dishes, models.Dishes.submenu_id == models.SubMenus.id)
            .group_by(models.SubMenus.id)
            .subquery()
        )

        query = (
            select(
                models.Menus.id.label('menu_id'),
                models.Menus.title.label('menu_title'),
                models.Menus.description.label('menu_description'),
                submenus_count.c.submenus_count.label('menu_submenus_count'),
                dishes_count.c.dishes_count.label('menu_dishes_count'),
                models.SubMenus.id.label('submenu_id'),
                models.SubMenus.title.label('submenu_title'),
                models.SubMenus.description.label('submenu_description'),
                dishes_in_submenu_count.c.dishes_in_submenu_count.label('dishes_in_submenu_count'),
                models.Dishes.id.label('dish_id'),
                models.Dishes.title.label('dish_title'),
                func.cast(models.Dishes.price.label('dish_price'), String),
                models.Dishes.description.label('dish_description'),
            )
            .outerjoin(models.SubMenus, models.Menus.id == models.SubMenus.menu_id)
            .outerjoin(models.Dishes, models.SubMenus.id == models.Dishes.submenu_id)
            .outerjoin(submenus_count, submenus_count.c.menu_id == models.Menus.id)
            .outerjoin(dishes_count, dishes_count.c.menu_id == models.Menus.id)
            .outerjoin(dishes_in_submenu_count, dishes_in_submenu_count.c.id == models.SubMenus.id)

        )
        result = await self._session.execute(query)
        return result.mappings().all()
