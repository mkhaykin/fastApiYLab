from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from pydantic import Field


class BaseSubMenus(BaseModel):
    title: str
    description: Optional[str]


class CreateSubMenus(BaseSubMenus):
    menu_id: Optional[UUID] = None


class UpdateSubMenus(BaseSubMenus):
    pass


class SubMenus(CreateSubMenus):
    id: UUID
