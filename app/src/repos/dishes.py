from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import crud, schemas
from app.src.database import get_db

from .base import BaseRepository
from .menus import MenuRepository
from .submenus import SubMenuRepository


class DishesRepository(BaseRepository):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        super().__init__(session)
        self._crud = crud.DishesCRUD(session)

    async def get_by_ids(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID | None = None) -> list[schemas.GetDish]:
        items = await crud.DishesCRUD(self._session).get_by_ids(menu_id, submenu_id, dish_id)
        return [schemas.GetDish(**item) for item in items]

    async def create_dish(self, menu_id: UUID, submenu_id: UUID, dish: schemas.CreateDishIn) -> schemas.CreateDishOut:
        # assert obj.menu_id
        if not (await MenuRepository(self._session).get(menu_id)):
            raise HTTPException(404, 'menu not found')

        if not (await SubMenuRepository(self._session).get(submenu_id)):
            raise HTTPException(404, 'submenu not found')

        return schemas.CreateDishOut(**await self._create(**{'submenu_id': submenu_id, **dish.model_dump()}))

    async def update_dish(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID,
                          dish: schemas.UpdateDishIn) -> schemas.UpdateDishOut:
        if not (await MenuRepository(self._session).get(menu_id)):
            raise HTTPException(404, 'menu not found')
        if not (await SubMenuRepository(self._session).get(submenu_id)):
            raise HTTPException(404, 'submenu not found')

        return schemas.UpdateDishOut(**await self._update(dish_id, **dish.model_dump()))

    async def delete_dish(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
        # check menu exists
        if not (await MenuRepository(self._session).get(menu_id)):
            raise HTTPException(404, 'menu not found')
        if not (await SubMenuRepository(self._session).get(submenu_id)):
            raise HTTPException(404, 'submenu not found')

        await self._delete(dish_id)
        # await cache_del(menu_id, 'menu')  # TODO
        return
