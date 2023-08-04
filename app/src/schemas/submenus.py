from uuid import UUID

from pydantic import BaseModel


class BaseSubMenus(BaseModel):
    title: str
    description: str | None


class CreateSubMenus(BaseSubMenus):
    menu_id: UUID | None = None


class UpdateSubMenus(BaseSubMenus):
    pass


class SubMenus(CreateSubMenus):
    id: UUID
