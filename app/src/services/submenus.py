from uuid import UUID

from fastapi import Depends, HTTPException

from app.src import schemas
from app.src.repos import SubMenuRepository

from .base import BaseService


class SubMenusService(BaseService):
    def __init__(self, repo: SubMenuRepository = Depends()):
        self.repo = repo

    # async def _get_submenu_with_check(self, menu_id: UUID, submenu_id: UUID) -> models.SubMenus | dict:
    #     # TODO FIX! не нужно это тут
    #     # CHECK menu_id == repo_menu.menu_id ??? HOW ???
    #     repo_submenu = await self.repo.get(submenu_id)
    #     # TODO костыль, не правильно бросаем объекты: надо или дикты или пиклить сами объекты, а тут то дикт, то объект
    #     # исправится автоматом если увести на уровень репозитория
    #     if isinstance(repo_submenu, models.SubMenus) and repo_submenu.menu_id != menu_id:
    #         raise HTTPException(status_code=404, detail='menu not found')
    #     return repo_submenu

    # async def get_all(self) -> list[schemas.GetMenu]:
    #     return await self.repo.get_by_ids()

    async def get_all(self, menu_id: UUID) -> list[schemas.GetSubMenu]:
        return await self.repo.get_by_ids(menu_id)

    async def get(self, menu_id: UUID, submenu_id: UUID) -> schemas.GetSubMenu | None:
        # return await self._get_submenu_with_check(menu_id, submenu_id)
        result = await self.repo.get_by_ids(menu_id, submenu_id)
        if len(result) == 0:
            raise HTTPException(404, 'submenu not found')
        return result[0]    # TODO check if more one

    async def create(self, menu_id: UUID, submenu: schemas.CreateSubMenuIn) -> schemas.CreateSubMenuOut:
        # if not submenu.menu_id:
        #     submenu.menu_id = menu_id   # ignore menu_id in submenu
        # if menu_id and submenu.menu_id and menu_id != submenu.menu_id:
        #     HTTPException(400, "error while creating submenus (\"menu_id != submenu.menu_id\"")
        result = await self.repo.create_submenu(menu_id, submenu)
        return result

    async def update(self, menu_id: UUID, submenu_id: UUID, submenu: schemas.UpdateSubMenuIn) -> schemas.UpdateSubMenuIn:
        # check menu_id equal submenu.menu_id
        # _ = await self._get_submenu_with_check(menu_id, submenu_id)
        return await self.repo.update_submenu(menu_id, submenu_id, submenu)

    async def delete(self, menu_id: UUID, submenu_id: UUID) -> None:
        # # check menu_id equal submenu.menu_id
        # _ = await self._get_submenu_with_check(menu_id, submenu_id)
        # result = await self.repo.delete(menu_id, submenu_id)
        return await self.repo.delete_submenu(menu_id, submenu_id)
