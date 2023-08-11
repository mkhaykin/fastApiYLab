from decimal import Decimal
from uuid import UUID

from .base import BaseSchema

DISH_PRICE_ENCODER = {float: lambda x: f'{round(float(x), 2):.2f}'}


class BaseDish(BaseSchema):
    title: str
    description: str | None = None
    price: str | Decimal
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


class GetDish(BaseDish):
    id: UUID
    submenu_id: UUID
    pass


class CreateDishIn(BaseDish):
    price: str | Decimal
    pass


class CreateDishOut(CreateDishIn):
    id: UUID
    submenu_id: UUID
    price: str | Decimal
    pass


class UpdateDishIn(BaseDish):
    pass


class UpdateDishOut(UpdateDishIn):
    id: UUID


class Dish(GetDish):
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
