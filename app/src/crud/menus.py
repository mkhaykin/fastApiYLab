from app.src import models

from .base import CRUDBase


class CRUDMenus(CRUDBase):
    def __init__(self):
        super().__init__(models.Menus, 'menu')


crud_menus = CRUDMenus()
