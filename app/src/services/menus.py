from uuid import UUID

from fastapi import Depends

from app.src import schemas
from app.src.repos import MenuRepository

from .base import BaseService


class MenusService(BaseService):
    def __init__(self, repo: MenuRepository = Depends()):
        self.repo = repo

    def get_all(self):
        return self.repo.get_all()

    def get(self, menu_id: UUID):
        return self.repo.get(menu_id)

    def create(self, menu: schemas.CreateMenu):
        return self.repo.create(menu)

    def update(self, menu_id: UUID, menu: schemas.UpdateMenu):
        return self.repo.update(menu_id, menu)

    def delete(self, menu_id: UUID):
        return self.repo.delete(menu_id)
