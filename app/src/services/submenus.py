from uuid import UUID

from fastapi import Depends, HTTPException

from app.src import schemas
from app.src.repos import SubMenuRepository

from .base import BaseService


class SubMenusService(BaseService):
    def __init__(self, repo: SubMenuRepository = Depends()):
        self.repo = repo

    def _get_submenu_with_check(self, menu_id: UUID, submenu_id: UUID):
        # CHECK menu_id == repo_menu.menu_id ??? HOW ???
        repo_submenu = self.repo.get(submenu_id)
        if repo_submenu.menu_id != menu_id:
            raise HTTPException(status_code=404, detail='menu not found')
        return repo_submenu

    def get_all(self):
        return self.repo.get_all()

    def get_by_menu(self, menu_id: UUID):
        return self.repo.get_by_menu(menu_id)

    def get(self, menu_id: UUID, submenu_id: UUID):
        return self._get_submenu_with_check(menu_id, submenu_id)

    def create(self, menu_id: UUID, submenu: schemas.CreateSubMenu):
        submenu.menu_id = menu_id   # ignore menu_id in submenu
        return self.repo.create(submenu)

    def update(self, menu_id: UUID, submenu_id: UUID, submenu: schemas.UpdateSubMenu):
        # check menu_id equal submenu.menu_id
        _ = self._get_submenu_with_check(menu_id, submenu_id)
        return self.repo.update(submenu_id, submenu)

    def delete(self, menu_id: UUID, submenu_id: UUID):
        # check menu_id equal submenu.menu_id
        _ = self._get_submenu_with_check(menu_id, submenu_id)
        return self.repo.delete(submenu_id)
