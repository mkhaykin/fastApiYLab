from uuid import UUID

from pydantic import BaseModel


class BaseMenu(BaseModel):
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


class Menu(BaseMenu):
    id: UUID
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


class CreateMenu(BaseMenu):
    pass


class UpdateMenu(BaseMenu):
    pass
