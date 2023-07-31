from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from pydantic import Field


class Dishes(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    title: str
    description: Optional[str] = None
    price: str


class UpdateDish(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[str]
