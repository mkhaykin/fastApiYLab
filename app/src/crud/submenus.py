from typing import Sequence
from uuid import UUID

from sqlalchemy import RowMapping, distinct, func, select

from app.src import models

from .base import BaseCRUD


class SubMenusCRUD(BaseCRUD):
    _model = models.SubMenus
    _name_for_error = 'submenu'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._base_select = (
            select(
                models.SubMenus.id,
                models.SubMenus.menu_id,
                models.SubMenus.title,
                models.SubMenus.description,
                func.count(distinct(models.Dishes.id)).label('dishes_count'),
            )
            .outerjoin(models.Dishes, models.SubMenus.id == models.Dishes.submenu_id)
            .group_by(models.SubMenus.id)
        )

    async def get_by_ids(self, menu_id: UUID, submenu_id: UUID | None = None) -> Sequence[RowMapping]:
        query = (
            self.base_select
            .where(self.model.menu_id == menu_id))
        if submenu_id:
            query = query.where(self.model.id == submenu_id)
        db_submenus = (await self._session.execute(query))
        return db_submenus.mappings().all()
