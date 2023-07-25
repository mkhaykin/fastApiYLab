from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import app.src.models as models
from ..database import get_db
from ..schemas import Dishes as SchemaDishes
from ..schemas import UpdateDish as SchemaUpdateDishes


router = APIRouter()


# GET /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes
@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
async def get_dishes(menu_id: UUID, submenu_id: UUID, db: Session = Depends(get_db)):
    db_menu = db.query(models.Menus).filter(models.Menus.id == menu_id).first()
    if not db_menu:
        return []
        # raise HTTPException(status_code=404, detail="menu not found")

    db_submenu = (
        db.query(models.SubMenus)
        .filter(models.SubMenus.menu_id == menu_id, models.SubMenus.id == submenu_id)
        .first()
    )
    if not db_submenu:
        return []
        # raise HTTPException(status_code=404, detail="submenu not found")

    db_dishes = (
        db.query(models.Dishes).filter(models.Dishes.submenu_id == submenu_id).all()
    )
    return jsonable_encoder(db_dishes, custom_encoder={float: str})


# GET /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes/{{api_test_dish_id}}
@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def get_dish(
    menu_id: UUID, submenu_id: UUID, dish_id: UUID, db: Session = Depends(get_db)
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

    db_dish = (
        db.query(models.Dishes)
        .filter(models.Dishes.id == dish_id, models.Dishes.submenu_id == submenu_id)
        .first()
    )
    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    return jsonable_encoder(db_dish, custom_encoder={float: str})


# POST /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes
@router.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=201)
async def create_dish(
    menu_id: UUID, submenu_id: UUID, dishes: SchemaDishes, db: Session = Depends(get_db)
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

    db_dish = models.Dishes(**dishes.model_dump(), submenu_id=submenu_id)
    try:
        db.add(db_dish)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"the dish is duplicated")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=424, detail=f"DB error while creating dish")

    db.refresh(db_dish)
    return jsonable_encoder(db_dish, custom_encoder={float: str})


# PATCH /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes/{{api_test_dish_id}}
@router.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=200
)
async def patch_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish: SchemaUpdateDishes,
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

    db_dish = (
        db.query(models.Dishes)
        .filter(models.Dishes.submenu_id == submenu_id, models.Dishes.id == dish_id)
        .first()
    )
    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")
    try:
        for column, value in dish.model_dump(exclude_unset=True).items():
            setattr(db_dish, column, value)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"the dish is duplicated")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=424, detail=f"DB error while update submenu")

    db.refresh(db_dish)
    return jsonable_encoder(db_dish, custom_encoder={float: str})


# DELETE /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes/{{api_test_dish_id}}
@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(
    menu_id: UUID, submenu_id: UUID, dish_id: UUID, db: Session = Depends(get_db)
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

    db_dish = (
        db.query(models.Dishes)
        .filter(models.Dishes.submenu_id == submenu_id, models.Dishes.id == dish_id)
        .first()
    )
    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    try:
        db.delete(db_dish)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=424, detail=f"DB error while deleting submenu")

    return
