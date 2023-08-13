from uuid import UUID

from .base import BaseSchema
from .dish import GetDish


class BaseSubMenu(BaseSchema):
    title: str
    description: str | None
    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': 'Submenu 1 title',
                    'description': 'Submenu 1 description',
                }
            ]
        }
    }


class GetSubMenu(BaseSubMenu):
    id: UUID
    menu_id: UUID
    dishes_count: int
    # menu_id: UUID | None = None
    pass


class GetSubMenuFull(BaseSubMenu):
    id: UUID
    menu_id: UUID
    dishes_count: int
    dishes: list[GetDish] | None
    pass


class CreateSubMenuIn(BaseSubMenu):
    pass


class CreateSubMenu(CreateSubMenuIn):
    menu_id: UUID


class CreateSubMenuOut(CreateSubMenu):
    id: UUID


class UpdateSubMenuIn(BaseSubMenu):
    pass


class UpdateSubMenuOut(UpdateSubMenuIn):
    id: UUID
    menu_id: UUID


class SubMenu(GetSubMenu):
    # model_config = {
    #     'json_schema_extra': {
    #         'examples': [
    #             {
    #                 'id': '3e5864f3-ddf0-4be8-b563-a9151e9ee85e',
    #                 'menu_id': '325523fe-17a5-4f46-bb0a-3cf6d397a182',
    #                 'title': 'Submenu 1 title',
    #                 'description': 'Submenu 1 description',
    #                 'dishes_count': 5,
    #             }
    #         ]
    #     }
    # }
    pass
