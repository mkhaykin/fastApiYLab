from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import models

from .base import CRUDBase


class CRUDSubMenus(CRUDBase):
    def __init__(self):
        super().__init__(models.SubMenus, 'submenu')

    async def get_by_menu(self, menu_id: UUID, db: AsyncSession):
        query = select(self.model).where(self.model.menu_id == menu_id)
        db_submenus = (await db.execute(query)).scalars().all()
        return db_submenus


crud_submenus = CRUDSubMenus()
