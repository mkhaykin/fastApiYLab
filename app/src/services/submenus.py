from uuid import UUID

from fastapi import Depends, HTTPException

from app.src import schemas
from app.src.cache.actions import cache_del
from app.src.repos import SubMenuRepository

from .base import BaseService


class SubMenusService(BaseService):
    def __init__(self, repo: SubMenuRepository = Depends()):
        self.repo = repo

    async def _get_submenu_with_check(self, menu_id: UUID, submenu_id: UUID):
        # TODO FIX! не нужно это тут
        # CHECK menu_id == repo_menu.menu_id ??? HOW ???
        repo_submenu = await self.repo.get(submenu_id)
        if repo_submenu.menu_id != menu_id:
            raise HTTPException(status_code=404, detail='menu not found')
        return repo_submenu

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_menu(self, menu_id: UUID):
        return await self.repo.get_by_menu(menu_id)

    async def get(self, menu_id: UUID, submenu_id: UUID):
        return await self._get_submenu_with_check(menu_id, submenu_id)

    async def create(self, menu_id: UUID, submenu: schemas.CreateSubMenu):
        submenu.menu_id = menu_id   # ignore menu_id in submenu
        result = await self.repo.create_submenu(submenu)
        await cache_del(menu_id)
        return result

    async def update(self, menu_id: UUID, submenu_id: UUID, submenu: schemas.UpdateSubMenu):
        # check menu_id equal submenu.menu_id
        _ = await self._get_submenu_with_check(menu_id, submenu_id)
        return await self.repo.update(submenu_id, submenu)

    async def delete(self, menu_id: UUID, submenu_id: UUID):
        # check menu_id equal submenu.menu_id
        _ = await self._get_submenu_with_check(menu_id, submenu_id)
        result = await self.repo.delete(submenu_id)
        await cache_del(menu_id)
        return result
