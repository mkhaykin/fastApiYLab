from uuid import UUID

from fastapi import Depends, HTTPException

from app.src import schemas
from app.src.cache.actions import cache_del
from app.src.repos import DishesRepository

from .base import BaseService


class DishesService(BaseService):
    def __init__(self, repo: DishesRepository = Depends()):
        self.repo = repo

    async def get_all(self, menu_id: UUID, submenu_id: UUID) -> list[schemas.GetDish]:
        return await self.repo.get_by_ids(menu_id, submenu_id)

    async def get(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> schemas.GetDish | None:
        await self.repo.check(menu_id, submenu_id)
        result = await self.repo.get_by_ids(menu_id, submenu_id, dish_id)
        if len(result) == 0:
            raise HTTPException(404, 'dish not found')
        return result[0]  # TODO check if more one

    async def create(self, menu_id: UUID, submenu_id: UUID, dish: schemas.CreateDishIn) -> schemas.CreateDishOut:
        await self.repo.check(menu_id, submenu_id)
        result = await self.repo.create_dish(menu_id, submenu_id, dish)
        await cache_del(menu_id, 'menu')
        await cache_del(submenu_id, 'submenu')
        return result

    async def update(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID,
                     submenu: schemas.UpdateDishIn) -> schemas.UpdateDishIn:
        await self.repo.check(menu_id, submenu_id)
        return await self.repo.update_dish(menu_id, submenu_id, dish_id, submenu)

    async def delete(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
        await self.repo.check(menu_id, submenu_id)
        await self.repo.delete_dish(menu_id, submenu_id, dish_id)
