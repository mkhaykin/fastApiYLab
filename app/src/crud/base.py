from typing import Any, TypeVar
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import Result, Select, select
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import models


class BaseCRUD:
    _model: type[models.BaseModel] = models.BaseModel
    _base_select: Select | None = None
    _name_for_error: str = ''
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    @property
    def model(self) -> type[models.TBaseModel]:
        return self._model

    @property
    def base_select(self) -> Select:
        return self._base_select if self._base_select is not None else select(self.model)

    @property
    def name_for_error(self) -> str:
        return self._name_for_error if self._name_for_error else str(self._model.__tablename__)

    async def get_all(self) -> Result[Any]:
        """
        Базовая заготовка для получения всех данных
        :return: результат select
        """
        return await self._session.execute(self.base_select)

    async def get(self, obj_id: UUID) -> Result[Any]:
        """
        Базовая заготовка для получения данных по выбранному объекту
        :param obj_id: код объекта
        :return: результат select
        """
        return await self._session.execute(self.base_select.where(self.model.id == obj_id))

    async def get_by_id(self, obj_id: UUID) -> models.TBaseModel:
        """
        Возврат
        :param obj_id:
        :return: модель объекта или HTTPException, если не найден
        """
        db_obj: models.BaseModel = (await self._session.get(self.model, obj_id))
        if not db_obj:
            raise HTTPException(404, f'{self._name_for_error} not found')
        return db_obj

    # async def create(self, obj: schemas.BaseSchema) -> models.TBaseModel:
    #     db_obj: models.BaseModel = self.model(**obj.model_dump())
    #     try:
    #         self._session.add(db_obj)
    #         await self._session.commit()
    #         await self._session.refresh(db_obj)
    #     except IntegrityError:
    #         await self._session.rollback()
    #         raise Exception(409, f'the {self._name_for_error} is duplicated')
    #     except Exception:
    #         await self._session.rollback()
    #         raise Exception(424, f'DB error while creating {self._name_for_error}')
    #     return db_obj

    async def create2(self, **kwargs) -> models.TBaseModel:
        db_obj: models.BaseModel = self.model(**kwargs)
        print(kwargs)
        try:
            self._session.add(db_obj)
            await self._session.commit()
            await self._session.refresh(db_obj)
        except IntegrityError as e:
            await self._session.rollback()
            print(e)
            raise HTTPException(409, f'the {self._name_for_error} is duplicated')
        except DatabaseError as e:
            await self._session.rollback()
            print(e)
            raise HTTPException(424, f'DB error while creating {self._name_for_error}')
        # TODO write log if Exception
        return db_obj

    # async def update(self, obj_id: UUID, obj: schemas.BaseSchema) -> models.TBaseModel:
    #     db_obj: models.BaseModel = (await self.get_by_id(obj_id))
    #     try:
    #         for column, value in obj.model_dump(exclude_unset=True).items():
    #             setattr(db_obj, column, value)
    #         await self._session.commit()
    #         await self._session.refresh(db_obj)
    #     except IntegrityError:
    #         await self._session.rollback()
    #         raise Exception(409, f'the {self._name_for_error} is duplicated')
    #     except Exception:
    #         await self._session.rollback()
    #         raise Exception(424, f'DB error while update {self._name_for_error}')
    #
    #     return db_obj

    async def update2(self, obj_id: UUID, **kwargs) -> models.TBaseModel:
        db_obj: models.BaseModel = (await self.get_by_id(obj_id))
        try:
            for column, value in kwargs.items():
                setattr(db_obj, column, value)
            await self._session.commit()
            await self._session.refresh(db_obj)
        except IntegrityError:
            await self._session.rollback()
            raise HTTPException(409, f'the {self._name_for_error} is duplicated')
        except DatabaseError:
            await self._session.rollback()
            raise HTTPException(424, f'DB error while update {self._name_for_error}')
        # TODO write log if Exception

        return db_obj

    async def delete(self, obj_id: UUID) -> None:
        db_obj: models.BaseModel = await self.get_by_id(obj_id)

        try:
            await self._session.delete(db_obj)
            await self._session.commit()
        except DatabaseError:
            await self._session.rollback()
            raise HTTPException(424, f'DB error while deleting {self._name_for_error}')
        # TODO write log if Exception

        return


TBaseCRUD = TypeVar('TBaseCRUD', bound=BaseCRUD)
