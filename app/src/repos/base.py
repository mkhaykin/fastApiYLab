from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import crud, models
from app.src.cache import Cache, get_cache
from app.src.database import get_db


class BaseRepository:
    _crud: crud.BaseCRUD
    _session: AsyncSession
    _name: str = 'base'

    def __init__(
            self,
            session: AsyncSession = Depends(get_db),
            cache: Cache = Depends(get_cache)
    ):
        self._crud = crud.BaseCRUD(session)
        self._session = session  # TODO ? need ?
        self._cache = cache

    async def get_all(self):
        # TODO: check unused !
        return (await self._crud.get_all()).mappings().all()

    async def _create(self, **kwargs) -> dict:
        db_obj: models.BaseModel = await self._crud.create(**kwargs)
        return db_obj.__dict__

    async def _update(self, obj_id: UUID, **kwargs) -> dict:
        db_obj: models.BaseModel = await self._crud.update(obj_id, **kwargs)
        return db_obj.__dict__

    async def _delete(self, obj_id: UUID) -> None:
        return await self._crud.delete(obj_id)
