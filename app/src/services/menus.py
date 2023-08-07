from uuid import UUID

from fastapi import Depends

from app.src import schemas
from app.src.repos import MenuRepository

from .base import BaseService


class MenusService(BaseService):
    def __init__(self, repo: MenuRepository = Depends()):
        self.repo = repo

    async def get_all(self):
        return await self.repo.get_all()

    async def get(self, menu_id: UUID):
        return await self.repo.get(menu_id)

    async def create(self, menu: schemas.CreateMenu):
        return await self.repo.create(menu)

    async def update(self, menu_id: UUID, menu: schemas.UpdateMenu):
        return await self.repo.update(menu_id, menu)

    async def delete(self, menu_id: UUID):
        return await self.repo.delete(menu_id)
