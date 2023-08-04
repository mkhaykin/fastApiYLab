from uuid import uuid4

from sqlalchemy import Column, ForeignKey, String, UniqueConstraint, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property

from app.src.database import Base

from .dishes import Dishes


class SubMenus(Base):
    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    menu_id = Column(
        UUID(as_uuid=True), ForeignKey('menus.id', ondelete='CASCADE'), nullable=False
    )
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    dishes_count = column_property(
        select(func.count(Dishes.id))
        .where(Dishes.submenu_id == id)
        .correlate_except(Dishes)
        .scalar_subquery()
    )

    __table_args__ = (UniqueConstraint('menu_id', 'title', name='uc_sub_menu'),)
