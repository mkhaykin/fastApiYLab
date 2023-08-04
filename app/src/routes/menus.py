from fastapi import APIRouter
from fastapi import Depends

from app.src.database import get_db
from app.src import schemas
from .common import *

router = APIRouter()


# GET /app/v1/menus
@router.get("/api/v1/menus")
async def get_menus(db: Session = Depends(get_db)):
    return crud_menus.get_all(db)


# GET /app/v1/menus/{{api_test_menu_id}}
@router.get("/api/v1/menus/{menu_id}")
async def get_menu(menu_id: UUID, db: Session = Depends(get_db)):
    return menu_get(menu_id, db)


# POST /app/v1/menus
@router.post("/api/v1/menus", status_code=201)
async def create_menu(menu: schemas.CreateMenu, db: Session = Depends(get_db)):
    try:
        db_menu = crud_menus.create(menu, db=db)
    except Exception as e:
        raise HTTPException(status_code=e.args[0], detail=e.args[1])

    return db_menu


# PATCH /app/v1/menus/{{api_test_menu_id}}
@router.patch("/api/v1/menus/{menu_id}", status_code=200)
async def update_menu(
    menu_id: UUID, menu: schemas.UpdateMenu, db: Session = Depends(get_db)
):
    try:
        db_menu = crud_menus.update(menu_id, menu, db=db)
    except Exception as e:
        raise HTTPException(status_code=e.args[0], detail=e.args[1])
    return db_menu


# /app/v1/menus/{{api_test_menu_id}}
@router.delete("/api/v1/menus/{menu_id}")
async def delete_menu(menu_id: UUID, db: Session = Depends(get_db)):
    # check menu | submenu
    _ = menu_get(menu_id, db)

    try:
        crud_menus.delete(menu_id, db=db)
    except Exception as e:
        raise HTTPException(status_code=e.args[0], detail=e.args[1])
    return
