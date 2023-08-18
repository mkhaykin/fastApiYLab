from uuid import UUID

from fastapi import Depends, HTTPException

from app.src import schemas
from app.src.crud import DishesCRUD

from .base import BaseRepository
from .menus import MenuRepository
from .submenus import SubMenuRepository


class DishesRepository(BaseRepository):
    _crud: DishesCRUD
    _name: str = 'dish'

    def __init__(
            self,
            crud: DishesCRUD = Depends(),
            menu_repo: MenuRepository = Depends(),
            submenu_repo: SubMenuRepository = Depends(),
    ):
        super().__init__(crud)
        self._menu_repo = menu_repo
        self._submenu_repo = submenu_repo

    async def check(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish_id: UUID | None = None
    ) -> None:
        if not (await self._menu_repo.get_by_ids(menu_id)):
            raise HTTPException(404, 'menu not found')
        if not (await self._submenu_repo.get_by_ids(menu_id, submenu_id)):
            raise HTTPException(404, 'submenu not found')

        if dish_id and not (await self._crud.get_by_ids(menu_id, submenu_id, dish_id)):
            raise HTTPException(404, 'dish not found')

    async def get_by_ids(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish_id: UUID | None = None
    ) -> list[schemas.GetDish]:
        items = await self._crud.get_by_ids(menu_id, submenu_id, dish_id)
        result = [schemas.GetDish(**item) for item in items]
        return result

    async def create_dish(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish: schemas.CreateDishIn,
            obj_id: UUID | None = None,
    ) -> schemas.CreateDishOut:
        await self.check(menu_id, submenu_id)
        return schemas.CreateDishOut(
            **await self._create(**{'submenu_id': submenu_id, **dish.model_dump(), 'id': obj_id}))

    async def update_dish(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish_id: UUID,
            dish: schemas.UpdateDishIn
    ) -> schemas.UpdateDishOut:
        await self.check(menu_id, submenu_id)
        return schemas.UpdateDishOut(**await self._update(dish_id, **dish.model_dump()))

    async def delete_dish(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish_id: UUID
    ) -> None:
        await self.check(menu_id, submenu_id, dish_id)
        await self._delete(dish_id)
        return
