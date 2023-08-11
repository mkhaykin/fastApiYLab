from typing import TypeVar

from pydantic import BaseModel


class BaseSchema (BaseModel):
    pass


TBaseSchema = TypeVar('TBaseSchema', bound=BaseSchema)
