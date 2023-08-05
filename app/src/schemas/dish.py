from uuid import UUID

from pydantic import BaseModel


class BaseDish(BaseModel):
    title: str
    description: str | None = None
    price: str


class UpdateDish(BaseDish):
    pass


class CreateDish(BaseDish):
    submenu_id: UUID | None = None
    pass


class Dish(CreateDish):
    id: UUID
