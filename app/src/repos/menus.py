from fastapi import Depends
from sqlalchemy.orm import Session

from app.src.crud import CRUDMenus
from app.src.database import get_db

from .base import BaseRepository


class MenuRepository(BaseRepository):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(CRUDMenus(), db)
