from app.src import models
from .base import CRUDBase


class CRUDSubMenus(CRUDBase):
    def __init__(self):
        super().__init__(models.SubMenus, "submenu")

    def get_by_menu(self, menu_id, db):
        db_submenus = (
            db.query(self.model).filter(self.model.menu_id == menu_id).all()
        )
        return db_submenus


crud_submenus = CRUDSubMenus()
