from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.src.database import get_db
import app.src.models as models
from app.src.schemas import SubMenus as SchemaSubMenus
from app.src.schemas import UpdateSubMenu as SchemaUpdateSubMenu


router = APIRouter()


# GET /app/v1/menus/{{api_test_menu_id}}/submenus
@router.get("/api/v1/menus/{menu_id}/submenus")
async def get_submenus(menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(models.Menus).filter(models.Menus.id == menu_id).first()
    if not db_menu:
        return []
        # raise HTTPException(status_code=404, detail="menu not found")

    db_submenus = (
        db.query(models.SubMenus).filter(models.SubMenus.menu_id == menu_id).all()
    )
    return db_submenus


# GET /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}
@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def get_submenu(menu_id: UUID, submenu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(models.Menus).filter(models.Menus.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    db_submenu = (
        db.query(models.SubMenus)
        .filter(models.SubMenus.menu_id == menu_id, models.SubMenus.id == submenu_id)
        .first()
    )
    if not db_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    return db_submenu


# POST /app/v1/menus/{{api_test_menu_id}}/submenus
@router.post("/api/v1/menus/{menu_id}/submenus", status_code=201)
async def create_submenu(
    menu_id: UUID, submenu: SchemaSubMenus, db: Session = Depends(get_db)
):
    db_menu = db.query(models.Menus).filter(models.Menus.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    db_submenu = models.SubMenus(**submenu.model_dump(), menu_id=menu_id)
    try:
        db.add(db_submenu)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"the submenu is duplicated")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=424, detail=f"DB error while creating submenu")

    db.refresh(db_submenu)
    return db_submenu


# PATCH /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}
@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", status_code=200)
async def patch_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    menu: SchemaUpdateSubMenu,
    db: Session = Depends(get_db),
):
    db_menu = db.query(models.Menus).filter(models.Menus.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    db_submenu = (
        db.query(models.SubMenus)
        .filter(models.SubMenus.menu_id == menu_id, models.SubMenus.id == submenu_id)
        .first()
    )
    if not db_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    try:
        for column, value in menu.model_dump(exclude_unset=True).items():
            setattr(db_submenu, column, value)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"the submenu is duplicated")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=424, detail=f"DB error while update submenu")

    db.refresh(db_submenu)
    return db_submenu


# DELETE /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}
@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(
    menu_id: UUID, submenu_id: UUID, db: Session = Depends(get_db)
):
    db_menu = db.query(models.Menus).filter(models.Menus.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    db_submenu = (
        db.query(models.SubMenus)
        .filter(models.SubMenus.menu_id == menu_id, models.SubMenus.id == submenu_id)
        .first()
    )
    if not db_submenu:
        raise HTTPException(status_code=404, detail=f"submenu not found")

    try:
        db.delete(db_submenu)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=424, detail=f"DB error while deleting submenu")

    return
