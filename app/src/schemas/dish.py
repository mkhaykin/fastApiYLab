from uuid import UUID

from pydantic import BaseModel


class BaseDish(BaseModel):
    title: str
    description: str | None = None
    price: str
    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': 'Dish 1 title',
                    'description': 'Dish 1 description',
                    'price': '35.4',
                }
            ]
        }
    }


class UpdateDish(BaseDish):
    pass


class CreateDish(BaseDish):
    submenu_id: UUID | None = None
    pass


class Dish(CreateDish):
    id: UUID
    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '502006db-1df5-47c5-a319-0e5739e8955a',
                    'submenu_id': '1f0060ab-a360-434b-b2c2-14c9ac797e01',
                    'title': 'Dish 1 title',
                    'description': 'Dish 1 description',
                    'price': '35.4',
                }
            ]
        }
    }
