from app.src import models
from .base import CRUDBase


class CRUDDishes(CRUDBase):
    def __init__(self):
        super().__init__(models.Dishes, "dish")

    def get_by_submenu(self, submenu_id, db):
        db_dishes = (
            db.query(self.model).filter(self.model.submenu_id == submenu_id).all()
        )
        return db_dishes


crud_dishes = CRUDDishes()
