from uuid import UUID

from pydantic import Field

from .base import BaseSchema
from .dish import GetDish


class BaseSubMenu(BaseSchema):
    title: str = Field(examples=['Холодные закуски', 'К пиву'])
    description: str | None = Field(examples=['Рамен', 'Горячий рамен'])


class _BaseSubMenuID(BaseSubMenu):
    id: UUID
    menu_id: UUID


class _BaseSubMenuCount(BaseSubMenu):
    dishes_count: int = Field(examples=[6])


class GetSubMenu(_BaseSubMenuID, _BaseSubMenuCount):
    pass


class GetSubMenuFull(_BaseSubMenuID, _BaseSubMenuCount):
    dishes: list[GetDish]


class CreateSubMenuIn(BaseSubMenu):
    pass


class CreateSubMenu(CreateSubMenuIn):
    menu_id: UUID


class CreateSubMenuOut(_BaseSubMenuID):
    pass


class UpdateSubMenuIn(BaseSubMenu):
    pass


class UpdateSubMenuOut(_BaseSubMenuID):
    pass


class SubMenu(GetSubMenu):
    pass


class MessageSubMenuNotFound(BaseSchema):
    detail: str = 'submenu not found'


class MessageSubMenuDuplicated(BaseSchema):
    detail: str = 'the submenu is duplicated'


class MessageSubMenuDeleted(BaseSchema):
    detail: str = 'the submenu is deleted'
