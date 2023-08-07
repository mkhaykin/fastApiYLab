from typing import TypeVar
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.cache.actions import cache_del, cache_get, cache_set
from app.src.crud import CRUDBase
from app.src.database import Base

T = TypeVar('T', bound=Base)
CRUD = TypeVar('CRUD', bound=CRUDBase)
SCHEMA = TypeVar('SCHEMA', bound=BaseModel)


class BaseRepository:
    def __init__(self, crud: CRUD, db: AsyncSession):
        self.crud = crud
        self.db = db

    async def reset_cache(self):
        # drop all cached data for all CRUD object
        objs = await self.get_all()
        for obj in objs:
            await self.del_from_cache(obj)

    def get_cache_key(self, obj: Base) -> str:
        key: str = str(obj.__dict__['id'])
        return key

    async def add_to_cache(self, obj: Base):
        # add data to cache
        await cache_set(self.get_cache_key(obj), self.crud.name, obj)

    async def del_from_cache(self, obj_id: UUID):
        # drop cached data for id
        await cache_del(obj_id, self.crud.name)

    async def get_from_cache(self, obj_id: UUID):
        # drop cached data for id
        return await cache_get(obj_id, self.crud.name)

    async def get_all(self):
        return await self.crud.get_all(self.db)

    async def get(self, obj_id: UUID):
        cache_data = await self.get_from_cache(obj_id)
        if cache_data:
            return cache_data

        db_obj = await self.crud.get(obj_id, self.db)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f'{self.crud.name} not found')

        # await cache_set(obj_id, db_obj)
        await self.add_to_cache(db_obj)

        return db_obj

    async def create(self, obj: SCHEMA):
        try:
            db_obj = await self.crud.create(obj, self.db)
        except Exception as e:
            if len(e.args) != 2:
                raise HTTPException(status_code=500, detail=e)
            raise HTTPException(status_code=e.args[0], detail=e.args[1])

        # await cache_del(db_obj.id)
        await self.del_from_cache(db_obj.id)

        return db_obj

    async def update(self, obj_id: UUID, obj: SCHEMA):
        # await cache_del(obj_id)
        await self.del_from_cache(obj_id)
        try:
            db_obj = await self.crud.update(obj_id, obj, self.db)
        except Exception as e:
            raise HTTPException(status_code=e.args[0], detail=e.args[1])
        return db_obj

    async def delete(self, obj_id: UUID):
        await self.del_from_cache(obj_id)
        try:
            await self.crud.delete(obj_id, self.db)
        except Exception as e:
            raise HTTPException(status_code=e.args[0], detail=e.args[1])
        return
