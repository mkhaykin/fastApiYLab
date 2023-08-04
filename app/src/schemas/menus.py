from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from pydantic import Field


class BaseMenu(BaseModel):
    title: str
    description: Optional[str]


class Menus(BaseMenu):
    id: UUID


class CreateMenu(BaseMenu):
    pass


class UpdateMenu(BaseMenu):
    pass
