from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import crud, schemas
from app.src.cache import Cache, get_cache
from app.src.database import get_db

from .base import BaseRepository


class MenuRepository(BaseRepository):
    _crud: crud.MenusCRUD
    _name: str = 'menu'

    def __init__(self, session: AsyncSession = Depends(get_db), cache: Cache = Depends(get_cache)):
        super().__init__(session, cache)
        self._crud = crud.MenusCRUD(session)

    async def get_by_ids(self, menu_id: UUID | None = None) -> list[schemas.GetMenu]:
        if self._cache:
            cache: list[schemas.BaseSchema] | None
            cache = await self._cache.cache_get(f"{menu_id if menu_id else 'menu'}:None:None")
            if cache:
                return cache

        items = await crud.MenusCRUD(self._session).get_by_ids(menu_id)
        result = [schemas.GetMenu(**item) for item in items]

        await self._cache.cache_set(f"{menu_id if menu_id else 'menu'}:None:None", result)
        return result

    async def create_menu(self, obj: schemas.CreateMenuIn, obj_id: UUID | None = None) -> schemas.CreateMenuOut:
        return schemas.CreateMenuOut(**await self._create(**obj.model_dump(), id=obj_id))

    async def update_menu(self, menu_id: UUID, menu: schemas.UpdateMenuIn) -> schemas.UpdateMenuOut:
        if self._cache:
            await self._cache.cache_del_pattern(f'{menu_id}:*:*')
        return schemas.UpdateMenuOut(**await self._update(menu_id, **menu.model_dump()))

    async def delete_menu(self, menu_id: UUID) -> None:
        await self._delete(menu_id)
        if self._cache:
            await self._cache.cache_del_pattern(f'{menu_id}:*:*')
        return
