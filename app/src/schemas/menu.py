from uuid import UUID

from pydantic import BaseModel


class BaseMenu(BaseModel):
    title: str
    description: str | None


class Menu(BaseMenu):
    id: UUID


class CreateMenu(BaseMenu):
    pass


class UpdateMenu(BaseMenu):
    pass
