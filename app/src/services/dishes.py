from uuid import UUID

from fastapi import Depends

from app.src import schemas
from app.src.repos import DishesRepository

from .base import BaseService


class DishesService(BaseService):
    def __init__(
            self,
            repo: DishesRepository = Depends()
    ):
        self.repo = repo

    async def get_all(
            self,
            menu_id: UUID,
            submenu_id: UUID
    ) -> list[schemas.GetDish]:
        return await self.repo.get_by_ids(menu_id, submenu_id)

    async def get(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish_id: UUID
    ) -> schemas.GetDish | None:
        await self.repo.check(menu_id, submenu_id)
        result = await self.repo.get_by_ids(menu_id, submenu_id, dish_id)
        return self.get_one(result, 'dish not found')

    async def create(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish: schemas.CreateDishIn
    ) -> schemas.CreateDishOut:
        result = await self.repo.create_dish(menu_id, submenu_id, dish)
        return result

    async def update(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish_id: UUID,
            submenu: schemas.UpdateDishIn
    ) -> schemas.UpdateDishOut:
        return await self.repo.update_dish(menu_id, submenu_id, dish_id, submenu)

    async def delete(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish_id: UUID
    ) -> schemas.MessageDishDeleted:
        await self.repo.delete_dish(menu_id, submenu_id, dish_id)
        return schemas.MessageDishDeleted()
