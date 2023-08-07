from typing import Sequence
from uuid import UUID

from fastapi import Depends, HTTPException

from app.src import models, schemas
from app.src.cache.actions import cache_del
from app.src.repos import SubMenuRepository

from .base import BaseService


class SubMenusService(BaseService):
    def __init__(self, repo: SubMenuRepository = Depends()):
        self.repo = repo

    async def _get_submenu_with_check(self, menu_id: UUID, submenu_id: UUID) -> models.SubMenus | dict:
        # TODO FIX! не нужно это тут
        # CHECK menu_id == repo_menu.menu_id ??? HOW ???
        repo_submenu = await self.repo.get(submenu_id)
        # TODO костыль, не правильно бросаем объекты: надо или дикты или пиклить сами объекты, а тут то дикт, то объект
        # исправится автоматом если увести на уровень репозитория
        if isinstance(repo_submenu, models.SubMenus) and repo_submenu.menu_id != menu_id:
            raise HTTPException(status_code=404, detail='menu not found')
        return repo_submenu

    async def get_all(self) -> Sequence[models.SubMenus | dict]:
        return await self.repo.get_all()

    async def get_by_menu(self, menu_id: UUID) -> Sequence[models.SubMenus | dict]:
        return await self.repo.get_by_menu(menu_id)

    async def get(self, menu_id: UUID, submenu_id: UUID) -> models.SubMenus | dict:
        return await self._get_submenu_with_check(menu_id, submenu_id)

    async def create(self, menu_id: UUID, submenu: schemas.CreateSubMenu) -> models.SubMenus:
        submenu.menu_id = menu_id   # ignore menu_id in submenu
        result = await self.repo.create_submenu(submenu)
        await cache_del(menu_id, 'menu')
        return result

    async def update(self, menu_id: UUID, submenu_id: UUID, submenu: schemas.UpdateSubMenu) -> models.SubMenus:
        # check menu_id equal submenu.menu_id
        _ = await self._get_submenu_with_check(menu_id, submenu_id)
        return await self.repo.update(submenu_id, submenu)

    async def delete(self, menu_id: UUID, submenu_id: UUID) -> None:
        # check menu_id equal submenu.menu_id
        _ = await self._get_submenu_with_check(menu_id, submenu_id)
        result = await self.repo.delete(submenu_id)
        await cache_del(menu_id, 'menu')
        return result
