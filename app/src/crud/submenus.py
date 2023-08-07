from typing import Sequence, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import models

from .base import CRUDBase

T = TypeVar('T', bound=models.SubMenus)


class CRUDSubMenus(CRUDBase):
    def __init__(self):
        super().__init__(models.SubMenus, 'submenu')

    async def get_by_menu(self, menu_id: UUID, db: AsyncSession) -> Sequence[T]:
        query = select(self.model).where(self.model.menu_id == menu_id)
        db_submenus = (await db.execute(query)).scalars().all()
        return db_submenus


crud_submenus = CRUDSubMenus()
