from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from pydantic import Field


class BaseDishes(BaseModel):
    title: str
    description: Optional[str] = None
    price: str


class UpdateDishes(BaseDishes):
    pass


class CreateDishes(BaseDishes):
    submenu_id: Optional[UUID] = None
    pass


class Dishes(CreateDishes):
    id: UUID
