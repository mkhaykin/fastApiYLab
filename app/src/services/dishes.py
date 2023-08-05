from uuid import UUID

from fastapi import Depends, HTTPException

from app.src import schemas
from app.src.repos import DishesRepository

from .base import BaseService


class DishesService(BaseService):
    def __init__(self, repo: DishesRepository = Depends()):
        self.repo = repo

    def _get_dish_with_check(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
        repo_dish = self.repo.get(dish_id)
        if repo_dish.submenu_id != submenu_id:
            raise HTTPException(status_code=404, detail='submenu not found')

        return repo_dish

    def get_all(self):
        return self.repo.get_all()

    def get_by_submenu(self, menu_id: UUID, submenu_id: UUID):
        return self.repo.get_by_submenu(menu_id, submenu_id)

    def get(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
        # return self._get_dish_with_check(menu_id, submenu_id, dish_id)
        return self.repo.get_by_ids_path(menu_id, submenu_id, dish_id)

    def create(self, menu_id: UUID, submenu_id: UUID, dish: schemas.CreateDish):
        # TODO: check menu
        dish.submenu_id = submenu_id   # ignore menu_id in submenu
        return self.repo.create_with_menu(menu_id, dish)

    def update(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, submenu: schemas.UpdateDish):
        # check menu_id equal submenu.menu_id
        _ = self._get_dish_with_check(menu_id, submenu_id, dish_id)
        return self.repo.update(dish_id, submenu)

    def delete(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
        # check menu_id equal submenu.menu_id
        _ = self._get_dish_with_check(menu_id, submenu_id, dish_id)
        return self.repo.delete(dish_id)
