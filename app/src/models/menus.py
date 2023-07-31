from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy import select, func
from sqlalchemy.orm import column_property
from sqlalchemy.dialects.postgresql import UUID

from app.src.database import Base

from .submenus import SubMenus


class Menus(Base):
    __tablename__ = "menus"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    submenus_count = column_property(
        select(func.coalesce(func.count(SubMenus.id), 0))
        .where(SubMenus.menu_id == id)
        .correlate_except(SubMenus)
        .scalar_subquery()
    )

    dishes_count = column_property(
        select(func.coalesce(func.sum(SubMenus.dishes_count), 0))
        .where(SubMenus.menu_id == id)
        .correlate_except(SubMenus)
        .scalar_subquery()
    )
