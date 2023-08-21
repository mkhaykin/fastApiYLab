from decimal import Decimal
from uuid import UUID

from pydantic import Field, field_validator

from .base import BaseSchema

DISH_PRICE_ENCODER = {float: lambda x: f'{round(float(x), 2):.2f}'}


def str_to_int(raw: str) -> int:
    if not raw:
        return 0
    return int(raw)


class BaseDish(BaseSchema):
    title: str = Field(examples=['Сельдь Бисмарк', 'Традиционное немецкое блюдо из маринованной сельди'])
    description: str | None = Field(examples=['Мясная тарелка',
                                              'Нарезка из ветчины, колбасных колечек, нескольких '
                                              'сортов сыра и фруктовАлкогольные напитки'])
    price: Decimal = Field(examples=['182.99', '215.36'])

    discount: int | None = Field(examples=[10, 0], default=0)
    _discount = field_validator('discount', mode='before')(str_to_int)


class _BaseDishID(BaseDish):
    id: UUID
    submenu_id: UUID


class GetDish(_BaseDishID):
    pass


class CreateDishIn(BaseDish):
    pass


class CreateDish(BaseDish):
    submenu_id: UUID


class CreateDishOut(_BaseDishID):
    pass


class UpdateDishIn(BaseDish):
    pass


class UpdateDishOut(_BaseDishID):
    pass


class Dish(GetDish):
    pass


class MessageDishNotFound(BaseSchema):
    detail: str = 'dish not found'


class MessageDishDuplicated(BaseSchema):
    detail: str = 'the dish is duplicated'


class MessageDishDeleted(BaseSchema):
    detail: str = 'the dish is deleted'
