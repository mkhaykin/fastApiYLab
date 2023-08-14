from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import models
from app.src.crud import BaseCRUD
from app.src.database import get_db


class BaseRepository:
    _crud: BaseCRUD
    _session: AsyncSession
    _name: str = 'base'

    def __init__(
            self,
            session: AsyncSession = Depends(get_db),
            crud: BaseCRUD = Depends(),
    ):
        self._crud = crud
        self._session = session  # TODO ? need ?

    async def _create(self, **kwargs) -> dict:
        db_obj: models.BaseModel = await self._crud.create(**kwargs)
        return db_obj.__dict__

    async def _update(self, obj_id: UUID, **kwargs) -> dict:
        db_obj: models.BaseModel = await self._crud.update(obj_id, **kwargs)
        return db_obj.__dict__

    async def _delete(self, obj_id: UUID) -> None:
        return await self._crud.delete(obj_id)
