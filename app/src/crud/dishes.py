from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import models

from .base import CRUDBase


class CRUDDishes(CRUDBase):
    def __init__(self):
        super().__init__(models.Dishes, 'dish')

    async def get_by_submenu(self, submenu_id: UUID, db: AsyncSession):
        # TODO
        query = select(self.model).where(self.model.submenu_id == submenu_id)
        db_dishes = (await db.execute(query)).scalars().all()
        return db_dishes


crud_dishes = CRUDDishes()
