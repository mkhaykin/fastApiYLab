from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.src import schemas
from app.src.crud import CRUDMenus, CRUDSubMenus
from app.src.database import get_db

from .base import BaseRepository


class SubMenuRepository(BaseRepository):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(CRUDSubMenus(), db)
        # self.crud: CRUDSubMenus = CRUDSubMenus()
        # self.db: Session = db

    def get_by_menu(self, menu_id: UUID):
        return CRUDSubMenus().get_by_menu(menu_id, self.db)

    # def get_by_ids_path(self, menu_id: str, submenu_id: str):
    #     # TODO подумать (вроде не использовал)
    #     db_submenu = self.get(submenu_id)
    #     if db_submenu.menu_id != menu_id:
    #         raise HTTPException(status_code=404, detail=f'submenu not found')
    #
    #     return db_submenu

    def create(self, obj: schemas.CreateSubMenu):
        # check the menu exists
        assert obj.menu_id
        if not CRUDMenus().get(obj.menu_id, self.db):
            raise HTTPException(status_code=404, detail='menu not found')

        return super().create(obj)
