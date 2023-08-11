from uuid import UUID

from fastapi import Depends, HTTPException

from app.src import schemas
from app.src.cache.actions import cache_del
from app.src.repos import DishesRepository

from .base import BaseService


class DishesService(BaseService):
    def __init__(self, repo: DishesRepository = Depends()):
        self.repo = repo

    # async def _get_dish_with_check(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> Sequence[
    #     models.Dishes | dict]:
    #     # print(menu_id, submenu_id, dish_id)
    #     repo_dish = (await self.repo.get(dish_id))
    #     # if repo_dish.submenu_id != submenu_id:
    #     #     raise HTTPException(status_code=404, detail='submenu not found')
    #     return repo_dish
    #
    # # async def get_all(self) -> Sequence[models.Dishes | dict]:
    # #     return await self.repo.get_all()

    async def get_all(self, menu_id: UUID, submenu_id: UUID) -> list[schemas.GetDish]:
        return await self.repo.get_by_ids(menu_id, submenu_id)

    async def get(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> schemas.GetDish | None:
        # return await self.repo.get_by_ids_path(menu_id, submenu_id, dish_id)
        result = await self.repo.get_by_ids(menu_id, submenu_id, dish_id)
        if len(result) == 0:
            raise HTTPException(404, 'dish not found')
        return result[0]  # TODO check if more one

    async def create(self, menu_id: UUID, submenu_id: UUID, dish: schemas.CreateDishIn) -> schemas.CreateDishOut:
        # dish.submenu_id = submenu_id  # ignore menu_id in submenu
        result = await self.repo.create_dish(menu_id, submenu_id, dish)
        await cache_del(menu_id, 'menu')
        await cache_del(submenu_id, 'submenu')
        return result

    async def update(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID,
                     submenu: schemas.UpdateDishIn) -> schemas.UpdateDishIn:
        return await self.repo.update_dish(menu_id, submenu_id, dish_id, submenu)

    async def delete(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
        # check menu_id equal submenu.menu_id
        # _ = await self._get_dish_with_check(menu_id, submenu_id, dish_id)
        # result = await self.repo._delete(dish_id)
        # await cache_del(menu_id, 'menu')
        # await cache_del(submenu_id, 'submenu')
        # return result
        await self.repo.delete_dish(menu_id, submenu_id, dish_id)
