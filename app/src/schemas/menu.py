from uuid import UUID

from .base import BaseSchema


class BaseMenu(BaseSchema):
    title: str
    description: str | None
    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': 'Menu 1 title',
                    'description': 'Menu 1 description',
                }
            ]
        }
    }


class GetMenu(BaseMenu):
    id: UUID
    submenus_count: int
    dishes_count: int
    pass


class CreateMenuIn(BaseMenu):
    pass


class CreateMenuOut(CreateMenuIn):
    id: UUID


class UpdateMenuIn(BaseMenu):
    pass


class UpdateMenuOut(UpdateMenuIn):
    id: UUID


class Menu(GetMenu):
    # model_config = {
    #     'json_schema_extra': {
    #         'examples': [
    #             {
    #                 'menu_id': '1030ea37-d07e-47e6-a973-4b3c79f3da12',
    #                 'title': 'Menu 1 title',
    #                 'description': 'Menu 1 description',
    #                 'submenus_count': 1,
    #                 'dishes_count': 11
    #             }
    #         ]
    #     }
    # }
    pass
