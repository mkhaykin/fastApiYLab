from typing import Sequence
from uuid import UUID

from sqlalchemy import RowMapping, distinct, func, select

from app.src import models

from .base import BaseCRUD


class MenusCRUD(BaseCRUD):
    _model = models.Menus
    _name_for_error = 'menu'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
