from uuid import UUID

from pydantic import Field

from .base import BaseSchema
from .submenus import GetSubMenuFull


class BaseMenu(BaseSchema):
    title: str = Field(examples=['Меню', 'Алкогольное меню'])
    description: str | None = Field(examples=['Основное меню', 'Алкогольные напитки'])


class _BaseMenuID(BaseMenu):
    id: UUID


class _BaseMenuCount(BaseMenu):
    submenus_count: int = Field(examples=[2])
    dishes_count: int = Field(examples=[6])


class GetMenu(_BaseMenuID, _BaseMenuCount):
    pass


class GetMenuFull(_BaseMenuID, _BaseMenuCount):
    submenus: list[GetSubMenuFull | None] = Field(description='list of linked submenus')


class CreateMenuIn(BaseMenu):
    pass


class CreateMenuOut(_BaseMenuID):
    pass


class UpdateMenuIn(BaseMenu):
    pass


class UpdateMenuOut(_BaseMenuID):
    pass


class Menu(GetMenu):
    pass


class MessageMenuNotFound(BaseSchema):
    detail: str = 'menu not found'


class MessageMenuLoad(BaseSchema):
    detail: str = 'data loads manually'


class MessageMenuDuplicated(BaseSchema):
    detail: str = 'the menu is duplicated'


class MessageMenuDeleted(BaseSchema):
    detail: str = 'the menu is deleted'
