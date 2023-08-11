from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.src import crud, models, schemas
from app.src.database import get_db


class BaseRepository:
    _crud: crud.BaseCRUD
    _session: AsyncSession

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self._crud = crud.BaseCRUD(session)  # (session)
        self._session = session  # TODO ? need ?

    async def reset_cache(self):
        # drop all cached data for all CRUD object
        objs = await self.get_all()
        for obj in objs:
            await self.del_from_cache(obj)

    def get_cache_key(self, obj: models.BaseModel) -> str:
        key: str = str(obj.__dict__['id'])
        return key

    async def add_to_cache(self, obj: models.BaseModel) -> None:
        # add data to cache
        # await cache_set(self.get_cache_key(obj), self.crud.name, obj)
        return None

    async def del_from_cache(self, obj_id: UUID) -> None:
        # drop cached data for id
        # await cache_del(obj_id, self.crud.name)
        return None

    async def get_from_cache(self, obj_id: UUID) -> dict | None:
        # drop cached data for id
        # return await cache_get(obj_id, self.crud.name)
        return None

    async def get_all(self):
        # TODO: check unused !
        return (await self._crud.get_all()).mappings().all()

    async def get(self,
                  obj_id: UUID,
                  schema_obj: type[schemas.TBaseSchema] | None = None) \
            -> schemas.TBaseSchema | dict:
        cache_data = await self.get_from_cache(obj_id)
        if cache_data:
            return schema_obj(**cache_data) if schema_obj else cache_data

        db_obj: models.BaseModel = await self._crud.get_by_id(obj_id)
        dict_obj: dict = db_obj.__dict__
        # TODO cache
        # await self.add_to_cache(dict_obj)

        return schema_obj(**dict_obj) if schema_obj else dict_obj

    async def _create(self, **kwargs) -> dict:
        db_obj: models.BaseModel = await self._crud.create(**kwargs)
        await self.del_from_cache(db_obj.id)
        return db_obj.__dict__

    async def _update(self, obj_id: UUID, **kwargs) -> dict:
        await self.del_from_cache(obj_id)
        db_obj: models.BaseModel = await self._crud.update(obj_id, **kwargs)
        return db_obj.__dict__

    async def _delete(self, obj_id: UUID) -> None:
        await self.del_from_cache(obj_id)
        return await self._crud.delete(obj_id)
