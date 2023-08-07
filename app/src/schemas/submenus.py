from uuid import UUID

from pydantic import BaseModel


class BaseSubMenu(BaseModel):
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


class CreateSubMenu(BaseSubMenu):
    menu_id: UUID | None = None


class UpdateSubMenu(BaseSubMenu):
    pass


class SubMenu(CreateSubMenu):
    id: UUID
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
