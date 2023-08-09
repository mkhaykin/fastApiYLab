from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseModel


class SubMenus(BaseModel):
    menu_id = Column(
        UUID(as_uuid=True), ForeignKey('menus.id', ondelete='CASCADE'), nullable=False
    )

    __table_args__ = (UniqueConstraint('menu_id', 'title', name='uc_sub_menu'),)
