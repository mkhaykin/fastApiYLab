from typing import Sequence
from uuid import UUID

from sqlalchemy import RowMapping, select

from app.src import models

from .base import BaseCRUD


class DishesCRUD(BaseCRUD):
    _model: type[models.Dishes] = models.Dishes
    _name_for_error = 'dish'

    async def get_by_ids(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID | None = None) -> Sequence[RowMapping]:
        query = (
            select(models.Dishes.id,
                   models.Dishes.submenu_id,
                   models.Dishes.title,
                   models.Dishes.description,
                   models.Dishes.price, )
            .outerjoin(models.SubMenus, models.SubMenus.id == models.Dishes.submenu_id)
            .outerjoin(models.Menus, models.Menus.id == models.SubMenus.menu_id)
            .where(models.SubMenus.id == submenu_id, models.Menus.id == menu_id))
        if dish_id:
            query = query.where(self.model.id == dish_id)
        db_dishes = (await self._session.execute(query)).mappings().all()
        return db_dishes
