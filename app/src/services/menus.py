from typing import Sequence
from uuid import UUID

from fastapi import Depends

from app.src import models, schemas
from app.src.repos import MenuRepository

from .base import BaseService


class MenusService(BaseService):
    def __init__(self, repo: MenuRepository = Depends()):
        self.repo = repo

    async def get_all(self) -> Sequence[models.Menus | dict]:
        return await self.repo.get_all()

    async def get(self, menu_id: UUID) -> models.Menus | dict:
        return await self.repo.get(menu_id)

    async def create(self, menu: schemas.CreateMenu) -> models.Menus:
        return await self.repo.create(menu)

    async def update(self, menu_id: UUID, menu: schemas.UpdateMenu) -> models.Menus:
        return await self.repo.update(menu_id, menu)

    async def delete(self, menu_id: UUID) -> None:
        return await self.repo.delete(menu_id)
