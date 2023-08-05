from uuid import UUID

from pydantic import BaseModel


class BaseSubMenu(BaseModel):
    title: str
    description: str | None


class CreateSubMenu(BaseSubMenu):
    menu_id: UUID | None = None


class UpdateSubMenu(BaseSubMenu):
    pass


class SubMenu(CreateSubMenu):
    id: UUID
