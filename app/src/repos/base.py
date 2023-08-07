from typing import TypeVar
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.cache.actions import cache_del, cache_get, cache_set
from app.src.crud import CRUDBase

CRUD = TypeVar('CRUD', bound=CRUDBase)
SCHEMA = TypeVar('SCHEMA', bound=BaseModel)


class BaseRepository:
    def __init__(self, crud: CRUD, db: AsyncSession):
        self.crud = crud
        self.db = db

    async def get_all(self):
        return await self.crud.get_all(self.db)

    async def get(self, obj_id: UUID):
        cache_data = await cache_get(obj_id)
        if cache_data:
            return cache_data

        db_obj = await self.crud.get(obj_id, self.db)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f'{self.crud.name} not found')
        await cache_set(obj_id, db_obj)  # await

        return db_obj

    async def create(self, obj: SCHEMA):
        try:
            db_obj = await self.crud.create(obj, self.db)
        except Exception as e:
            if len(e.args) != 2:
                raise HTTPException(status_code=500, detail=e)
            raise HTTPException(status_code=e.args[0], detail=e.args[1])

        return db_obj

    async def update(self, obj_id: UUID, obj: SCHEMA):
        # await cache_del(obj_id)   # await
        try:
            db_obj = await self.crud.update(obj_id, obj, self.db)
        except Exception as e:
            raise HTTPException(status_code=e.args[0], detail=e.args[1])
        return db_obj

    async def delete(self, obj_id: UUID):
        await cache_del(obj_id)  # await
        try:
            await self.crud.delete(obj_id, self.db)
        except Exception as e:
            raise HTTPException(status_code=e.args[0], detail=e.args[1])
        return
