from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

from app.src import models
from app.src import schemas
from .base import CRUDBase


class CRUDMenus(CRUDBase):
    def __init__(self):
        super().__init__(models.Menus, "menu")


crud_menus = CRUDMenus()
