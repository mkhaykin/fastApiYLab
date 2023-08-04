from uuid import UUID

from pydantic import BaseModel


class BaseDishes(BaseModel):
    title: str
    description: str | None = None
    price: str


class UpdateDishes(BaseDishes):
    pass


class CreateDishes(BaseDishes):
    submenu_id: UUID | None = None
    pass


class Dishes(CreateDishes):
    id: UUID
