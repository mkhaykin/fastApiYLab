from uuid import UUID

from fastapi import Depends, HTTPException

from app.src import schemas
from app.src.repos import DishesRepository

from .base import BaseService


class DishesService(BaseService):
    def __init__(self, repo: DishesRepository = Depends()):
        self.repo = repo

    async def _get_dish_with_check(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
        repo_dish = await self.repo.get(dish_id)
        if repo_dish.submenu_id != submenu_id:
            raise HTTPException(status_code=404, detail='submenu not found')

        return repo_dish

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_submenu(self, menu_id: UUID, submenu_id: UUID):
        return await self.repo.get_by_submenu(menu_id, submenu_id)

    async def get(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
        # return self._get_dish_with_check(menu_id, submenu_id, dish_id)
        return await self.repo.get_by_ids_path(menu_id, submenu_id, dish_id)

    async def create(self, menu_id: UUID, submenu_id: UUID, dish: schemas.CreateDish):
        # TODO: check menu
        dish.submenu_id = submenu_id   # ignore menu_id in submenu
        return await self.repo.create_with_menu(menu_id, dish)

    async def update(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, submenu: schemas.UpdateDish):
        # check menu_id equal submenu.menu_id
        _ = await self._get_dish_with_check(menu_id, submenu_id, dish_id)
        return await self.repo.update(dish_id, submenu)

    async def delete(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
        # check menu_id equal submenu.menu_id
        _ = await self._get_dish_with_check(menu_id, submenu_id, dish_id)
        return await self.repo.delete(dish_id)
