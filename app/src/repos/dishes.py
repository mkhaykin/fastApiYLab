from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import crud, schemas
from app.src.cache import Cache, get_cache
from app.src.database import get_db

from .base import BaseRepository

# from .menus import MenuRepository
from .submenus import SubMenuRepository


class DishesRepository(BaseRepository):
    _crud: crud.DishesCRUD
    _name: str = 'dish'

    def __init__(
            self,
            session: AsyncSession = Depends(get_db),
            cache: Cache = Depends(get_cache),
            menu_repo: SubMenuRepository = Depends(),
            submenu_repo: SubMenuRepository = Depends(),
    ):
        super().__init__(session, cache)
        self._crud = crud.DishesCRUD(session)
        self._submenu_repo = submenu_repo
        self._menu_repo = menu_repo

    async def check(
            self,
            menu_id: UUID,
            submenu_id: UUID
    ) -> None:
        if not (await self._menu_repo.get_by_ids(menu_id)):
            raise HTTPException(404, 'menu not found')
        if not (await self._submenu_repo.get_by_ids(menu_id, submenu_id)):
            raise HTTPException(404, 'submenu not found')
        # if not (await MenuRepository(self._session, self._cache).get_by_ids(menu_id)):
        #     raise HTTPException(404, 'menu not found')
        # if not (await SubMenuRepository(self._session, self._cache).get_by_ids(menu_id, submenu_id)):
        #     raise HTTPException(404, 'submenu not found')

    async def get_by_ids(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish_id: UUID | None = None
    ) -> list[schemas.GetDish]:
        if self._cache:
            cache: list[schemas.BaseSchema] | None
            cache = await self._cache.get(f"{menu_id}:{submenu_id}:{dish_id if dish_id else 'dish'}")
            if cache:
                return cache

        items = await crud.DishesCRUD(self._session).get_by_ids(menu_id, submenu_id, dish_id)
        result = [schemas.GetDish(**item) for item in items]

        await self._cache.set(f"{menu_id}:{submenu_id}:{dish_id if dish_id else 'dish'}", result)
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

    async def update_dish(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID,
                          dish: schemas.UpdateDishIn) -> schemas.UpdateDishOut:
        await self.check(menu_id, submenu_id)
        return schemas.UpdateDishOut(**await self._update(dish_id, **dish.model_dump()))

    async def delete_dish(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish_id: UUID
    ) -> None:
        await self.check(menu_id, submenu_id)
        await self._delete(dish_id)
        return
