from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.src.database import get_db
import app.src.models as models
from app.src.schemas import Menus as SchemaMenus
from app.src.schemas import UpdateMenu as SchemaUpdateMenu


router = APIRouter()


# GET /app/v1/menus
@router.get("/api/v1/menus")
async def get_menus(db: Session = Depends(get_db)):
    return db.query(models.Menus).all()


# GET /app/v1/menus/{{api_test_menu_id}}
@router.get("/api/v1/menus/{menu_id}")
async def get_menu(menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(models.Menus).filter(models.Menus.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_menu


# POST /app/v1/menus
@router.post("/api/v1/menus", status_code=201)
async def create_menu(menu: SchemaMenus, db: Session = Depends(get_db)):
    db_menu = models.Menus(**menu.model_dump())  # TODO check id correct
    try:
        db.add(db_menu)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"the menu is duplicated")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=424, detail=f"DB error while creating menu")

    db.refresh(db_menu)
    return db_menu


# PATCH /app/v1/menus/{{api_test_menu_id}}
@router.patch("/api/v1/menus/{id}", status_code=200)
async def patch_menu(id: UUID, menu: SchemaUpdateMenu, db: Session = Depends(get_db)):
    query = db.query(models.Menus).filter(models.Menus.id == id)
    db_menu = query.first()
    if not db_menu:
        raise HTTPException(status_code=404, detail=f"menu not found")

    try:
        for column, value in menu.model_dump(exclude_unset=True).items():
            setattr(db_menu, column, value)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"the menu is duplicated")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=424, detail=f"DB error while update menu")

    db.refresh(db_menu)
    return db_menu


# /app/v1/menus/{{api_test_menu_id}}
@router.delete("/api/v1/menus/{menu_id}")
async def delete_menu(menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(models.Menus).filter(models.Menus.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail=f"menu not found")

    try:
        db.delete(db_menu)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=424, detail=f"DB error while deleting menu")

    return
