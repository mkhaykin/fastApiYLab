from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import crud, schemas
from app.src.database import get_db

from .base import BaseRepository


class MenuRepository(BaseRepository):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        super().__init__(session)
        self._crud = crud.MenusCRUD(session)

    async def get_by_ids(self, menu_id: UUID | None = None) -> list[schemas.GetMenu]:
        items = await crud.MenusCRUD(self._session).get_by_ids(menu_id)
        return [schemas.GetMenu(**item) for item in items]

    async def create_menu(self, obj: schemas.CreateMenuIn) -> schemas.CreateMenuOut:
        return schemas.CreateMenuOut(**await self._create(**obj.model_dump()))

    async def update_menu(self, menu_id: UUID, menu: schemas.UpdateMenuIn) -> schemas.UpdateMenuOut:
        return schemas.UpdateMenuOut(**await self._update(menu_id, **menu.model_dump()))

    async def delete_menu(self, menu_id: UUID) -> None:
        await self._delete(menu_id)
        # TODO удалить полный кэш (menu_id : submenu_id : dish_id)
        return
