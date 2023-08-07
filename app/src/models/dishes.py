from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Numeric, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID

from app.src.database import Base


class Dishes(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True), server_default=func.gen_random_uuid(), primary_key=True, default=uuid4,
                nullable=False, )
    submenu_id = Column(
        UUID(as_uuid=True),
        ForeignKey('submenus.id', ondelete='CASCADE'),
        nullable=False,
    )
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(
        Numeric(precision=10, scale=2, asdecimal=True, decimal_return_scale=None)
    )

    __table_args__ = (UniqueConstraint('submenu_id', 'title', name='uc_dishes'),)
