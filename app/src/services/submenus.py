from uuid import UUID

from fastapi import Depends

from app.src import schemas
from app.src.repos import SubMenuRepository

from .base import BaseService
from .dishes import DishesService


class SubMenusService(BaseService):
    def __init__(
            self,
            repo: SubMenuRepository = Depends(),
            service_dishes: DishesService = Depends()
    ):
        self.repo = repo
        self.service_dishes = service_dishes

    async def get_all(
            self,
            menu_id: UUID
    ) -> list[schemas.GetSubMenu]:
        return await self.repo.get_by_ids(menu_id)

    async def get_full(
            self,
            menu_id: UUID
    ) -> list[schemas.GetSubMenuFull | None]:
        result: list[schemas.GetSubMenuFull | None] = []
        submenus: list[schemas.GetSubMenu] = await self.repo.get_by_ids(menu_id)
        for submenu in submenus:
            result_submenus: schemas.GetSubMenuFull
            dishes = await self.service_dishes.get_all(menu_id, submenu.id)
            result_submenus = schemas.GetSubMenuFull(**submenu.model_dump(), dishes=dishes)
            result.append(result_submenus)
        return result

    async def get(
            self,
            menu_id: UUID,
            submenu_id: UUID
    ) -> schemas.GetSubMenu | None:
        result = await self.repo.get_by_ids(menu_id, submenu_id)
        return self.get_one(result, 'submenu not found')

    async def create(
            self,
            menu_id: UUID,
            submenu: schemas.CreateSubMenuIn
    ) -> schemas.CreateSubMenuOut:
        return await self.repo.create_submenu(menu_id, submenu)

    async def update(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            submenu: schemas.UpdateSubMenuIn
    ) -> schemas.UpdateSubMenuOut:
        return await self.repo.update_submenu(menu_id, submenu_id, submenu)

    async def delete(
            self,
            menu_id: UUID,
            submenu_id: UUID
    ) -> schemas.MessageMenuDeleted:
        await self.repo.delete_submenu(menu_id, submenu_id)
        return schemas.MessageMenuDeleted()
