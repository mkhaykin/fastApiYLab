# from sqlalchemy import Column, String, Numeric
# from sqlalchemy import ForeignKey
# from sqlalchemy import UniqueConstraint
# from sqlalchemy import select, func
# from sqlalchemy.orm import column_property
# from sqlalchemy.dialects.postgresql import UUID
# from uuid import uuid4
#
# from app.src.database import Base
#
#
# class Dishes(Base):
#     __tablename__ = "dishes"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
#     submenu_id = Column(
#         UUID(as_uuid=True),
#         ForeignKey("submenus.id", ondelete="CASCADE"),
#         nullable=False,
#     )
#     title = Column(String, unique=True, nullable=False)
#     description = Column(String, nullable=True)
#     price = Column(
#         Numeric(precision=10, scale=2, asdecimal=False, decimal_return_scale=None)
#     )
#
#     __table_args__ = (UniqueConstraint("submenu_id", "title", name="uc_dishes"),)
#
#
# class SubMenus(Base):
#     __tablename__ = "submenus"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
#     menu_id = Column(
#         UUID(as_uuid=True), ForeignKey("menus.id", ondelete="CASCADE"), nullable=False
#     )
#     title = Column(String, unique=True, nullable=False)
#     description = Column(String, nullable=True)
#
#     dishes_count = column_property(
#         select(func.count(Dishes.id))
#         .where(Dishes.submenu_id == id)
#         .correlate_except(Dishes)
#         .scalar_subquery()
#     )
#
#     __table_args__ = (UniqueConstraint("menu_id", "title", name="uc_sub_menu"),)
#
#
# class Menus(Base):
#     __tablename__ = "menus"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
#     title = Column(String, unique=True, nullable=False)
#     description = Column(String, nullable=True)
#
#     submenus_count = column_property(
#         select(func.coalesce(func.count(SubMenus.id), 0))
#         .where(SubMenus.menu_id == id)
#         .correlate_except(SubMenus)
#         .scalar_subquery()
#     )
#
#     dishes_count = column_property(
#         select(func.coalesce(func.sum(SubMenus.dishes_count), 0))
#         .where(SubMenus.menu_id == id)
#         .correlate_except(SubMenus)
#         .scalar_subquery()
#     )
