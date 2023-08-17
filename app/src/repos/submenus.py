from uuid import UUID

from fastapi import Depends, HTTPException

from app.src import schemas
from app.src.crud import SubMenusCRUD

from .base import BaseRepository
from .menus import MenuRepository


class SubMenuRepository(BaseRepository):
    _crud: SubMenusCRUD
    _name: str = 'submenu'

    def __init__(
            self,
            crud: SubMenusCRUD = Depends(),
            menu_repo: MenuRepository = Depends(),
    ):
        super().__init__(crud)
        self._menu_repo = menu_repo

    async def check(
            self,
            menu_id: UUID
    ):
        if not (await self._menu_repo.get_by_ids(menu_id)):
            raise HTTPException(status_code=404, detail='menu not found')

    async def get_by_ids(
            self,
            menu_id: UUID,
            submenu_id: UUID | None = None
    ) -> list[schemas.GetSubMenu]:
        items = await self._crud.get_by_ids(menu_id, submenu_id)
        result = [schemas.GetSubMenu(**item) for item in items]
        return result

    async def create_submenu(
            self,
            menu_id: UUID,
            menu: schemas.CreateSubMenuIn,
            obj_id: UUID | None = None,
    ) -> schemas.CreateSubMenuOut:
        await self.check(menu_id)
        return schemas.CreateSubMenuOut(**await self._create(**{'menu_id': menu_id, **menu.model_dump(), 'id': obj_id}))

    async def update_submenu(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            submenu: schemas.UpdateSubMenuIn
    ) -> schemas.UpdateSubMenuOut:
        await self.check(menu_id)
        return schemas.UpdateSubMenuOut(**await self._update(submenu_id, **submenu.model_dump()))

    async def delete_submenu(
            self,
            menu_id: UUID,
            submenu_id: UUID
    ):
        await self.check(menu_id)
        await self._delete(submenu_id)
