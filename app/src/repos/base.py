from typing import TypeVar
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.src.crud import CRUDBase

CRUD = TypeVar('CRUD', bound=CRUDBase)
SCHEMA = TypeVar('SCHEMA', bound=BaseModel)


class BaseRepository:
    def __init__(self, crud: CRUD, db: Session):
        self.crud = crud
        self.db = db

    def get_all(self):
        return self.crud.get_all(self.db)

    def get(self, obj_id: UUID):
        db_obj = self.crud.get(obj_id, self.db)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f'{self.crud.name} not found')
        return db_obj

    def create(self, obj: SCHEMA):
        try:
            db_obj = self.crud.create(obj, self.db)
        except Exception as e:
            raise HTTPException(status_code=e.args[0], detail=e.args[1])

        return db_obj

    def update(self, obj_id: UUID, obj: SCHEMA):
        try:
            db_obj = self.crud.update(obj_id, obj, self.db)
        except Exception as e:
            raise HTTPException(status_code=e.args[0], detail=e.args[1])

        return db_obj

    def delete(self, obj_id: UUID):
        try:
            self.crud.delete(obj_id, self.db)
        except Exception as e:
            raise HTTPException(status_code=e.args[0], detail=e.args[1])
        return
