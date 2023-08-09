from sqlalchemy import Column, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseModel


class Dishes(BaseModel):
    submenu_id = Column(
        UUID(as_uuid=True),
        ForeignKey('submenus.id', ondelete='CASCADE'),
        nullable=False,
    )

    price = Column(
        Numeric(precision=10, scale=2, asdecimal=True, decimal_return_scale=None)
    )

    __table_args__ = (UniqueConstraint('submenu_id', 'title', name='uc_dishes'),)
