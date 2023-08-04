from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.src import schemas
from app.src.crud import crud_submenus
from app.src.database import get_db

from .common import menu_get, submenu_get

router = APIRouter()


# GET /app/v1/menus/{{api_test_menu_id}}/submenus
@router.get('/api/v1/menus/{menu_id}/submenus')
async def get_submenus(menu_id: UUID, db: Session = Depends(get_db)):
    # check menu | submenu | dish
    try:
        _ = menu_get(menu_id, db)
    except Exception:
        return []
    return crud_submenus.get_by_menu(menu_id, db)


# GET /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}
@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def get_submenu(menu_id: UUID, submenu_id: UUID, db: Session = Depends(get_db)):
    # check menu | submenu and return
    return submenu_get(menu_id, submenu_id, db)


# POST /app/v1/menus/{{api_test_menu_id}}/submenus
@router.post('/api/v1/menus/{menu_id}/submenus', status_code=201)
async def create_submenu(
    menu_id: UUID, submenu: schemas.CreateSubMenus, db: Session = Depends(get_db)
):
    # check menu
    _ = menu_get(menu_id, db)

    if submenu.menu_id and submenu.menu_id != menu_id:
        raise HTTPException(status_code=424, detail='menu_id != menu_id')

    submenu.menu_id = menu_id
    try:
        db_submenu = crud_submenus.create(submenu, db=db)
    except Exception as e:
        raise HTTPException(status_code=e.args[0], detail=e.args[1])

    return db_submenu


# PATCH /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}
@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}', status_code=200)
async def patch_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu: schemas.UpdateSubMenus,
    db: Session = Depends(get_db),
):
    # check menu | submenu
    _ = submenu_get(menu_id, submenu_id, db)

    try:
        db_submenu = crud_submenus.update(submenu_id, submenu, db=db)
    except Exception as e:
        raise HTTPException(status_code=e.args[0], detail=e.args[1])
    return db_submenu


# DELETE /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}
@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu(
    menu_id: UUID, submenu_id: UUID, db: Session = Depends(get_db)
):
    # check menu | submenu
    _ = submenu_get(menu_id, submenu_id, db)

    try:
        crud_submenus.delete(submenu_id, db=db)
    except Exception as e:
        raise HTTPException(status_code=e.args[0], detail=e.args[1])
    return
