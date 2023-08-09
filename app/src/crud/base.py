from typing import Sequence, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.models.base import Base

T = TypeVar('T', bound=Base)


class CRUDBase:
    def __init__(self, model: type[T], name: str = ''):
        self.__model = model
        self.__name = name

    @property
    def model(self) -> type[T]:
        return self.__model

    @property
    def name(self) -> str:
        return self.__name

    async def get_all(self, db: AsyncSession) -> Sequence[T]:
        query = select(self.model)
        result = (await db.execute(query))
        return result.scalars().all()

    async def get(self, obj_id: UUID, db: AsyncSession) -> T:
        query = select(self.model).where(self.model.id == obj_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_id(self, obj_id: UUID, db: AsyncSession) -> T:
        query = select(self.model).where(self.model.id == obj_id)
        db_obj: Base = (await db.execute(query)).scalars().first()
        if not db_obj:
            raise Exception(404, f'{self.name} not found')
        return db_obj

    async def create(self, obj: BaseModel, db: AsyncSession) -> T:
        db_obj = self.model(**obj.model_dump())
        try:
            db.add(db_obj)
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise Exception(409, f'the {self.name} is duplicated')
        except Exception:
            await db.rollback()
            raise Exception(424, f'DB error while creating {self.name}')
        # await db.refresh(db_obj)
        return db_obj

    async def update(self, obj_id: UUID, obj: BaseModel, db: AsyncSession) -> T:
        db_obj: Base = await self.get_id(obj_id, db)

        try:
            for column, value in obj.model_dump(exclude_unset=True).items():
                setattr(db_obj, column, value)
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise Exception(409, f'the {self.name} is duplicated')
        except Exception:
            await db.rollback()
            raise Exception(424, f'DB error while update {self.name}')

        # await db.refresh(db_obj)
        return db_obj

    async def delete(self, obj_id: UUID, db: AsyncSession) -> None:
        db_obj: Base = await self.get_id(obj_id, db)

        try:
            await db.delete(db_obj)
            await db.commit()
        except Exception:
            await db.rollback()
            raise Exception(424, f'DB error while deleting {self.name}')

        return
