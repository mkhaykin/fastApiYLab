from uuid import UUID

from fastapi import Depends

from app.src import schemas
from app.src.cache.menus import CacheMenusHandler
from app.src.crud import MenusCRUD

from .base import BaseRepository


class MenuRepository(BaseRepository):
    _crud: MenusCRUD
    _name: str = 'menu'

    def __init__(
            self,
            crud: MenusCRUD = Depends(),
            cache_handler: CacheMenusHandler = Depends(),
    ):
        super().__init__(crud)
        self._cache_handler = cache_handler

    async def get_by_ids(
            self,
            menu_id: UUID | None = None
    ) -> list[schemas.GetMenu]:
        cache: list[schemas.GetMenu] | None
        cache = await self._cache_handler.get(menu_id)
        if cache:
            return cache

        items = await self._crud.get_by_ids(menu_id)
        result = [schemas.GetMenu(**item) for item in items]

        await self._cache_handler.add(menu_id, result)
        return result

    async def create_menu(
            self,
            obj: schemas.CreateMenuIn,
            obj_id: UUID | None = None
    ) -> schemas.CreateMenuOut:
        return schemas.CreateMenuOut(**await self._create(**obj.model_dump(), id=obj_id))

    async def update_menu(
            self,
            menu_id: UUID,
            menu: schemas.UpdateMenuIn
    ) -> schemas.UpdateMenuOut:
        return schemas.UpdateMenuOut(**await self._update(menu_id, **menu.model_dump()))

    async def delete_menu(
            self,
            menu_id: UUID
    ) -> None:
        await self._delete(menu_id)
        return
