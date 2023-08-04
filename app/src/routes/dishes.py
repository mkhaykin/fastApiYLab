from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.src import schemas
from app.src.crud import crud_dishes
from app.src.database import get_db

from .common import dish_get, submenu_get

router = APIRouter()


# GET /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes
@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
async def get_dishes(menu_id: UUID, submenu_id: UUID, db: Session = Depends(get_db)):
    # check menu | submenu | dish
    try:
        db_submenu = submenu_get(menu_id, submenu_id, db)
    except Exception:
        return []
    db_dishes = crud_dishes.get_by_submenu(submenu_id, db=db)
    if not db_dishes or not db_submenu or db_submenu.menu_id != menu_id:
        return []
    return jsonable_encoder(db_dishes, custom_encoder={float: str})


# GET /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes/{{api_test_dish_id}}
@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def get_dish(
        menu_id: UUID, submenu_id: UUID, dish_id: UUID, db: Session = Depends(get_db)
):
    db_dish = dish_get(menu_id, submenu_id, dish_id, db)
    return jsonable_encoder(db_dish, custom_encoder={float: str})


# POST /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes
@router.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', status_code=201)
async def create_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dishes: schemas.CreateDishes,
        db: Session = Depends(get_db),
):
    # check menu | submenu
    _ = submenu_get(menu_id, submenu_id, db)

    # submenu_id in schema must be equal submenu_id in arguments
    if dishes.submenu_id and dishes.submenu_id != submenu_id:
        raise HTTPException(status_code=424, detail="submenu_id's are different")
    dishes.submenu_id = submenu_id

    try:
        db_dish = crud_dishes.create(dishes, db=db)
    except Exception as e:
        raise HTTPException(status_code=e.args[0], detail=e.args[1])

    return jsonable_encoder(db_dish, custom_encoder={float: str})


# PATCH /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes/{{api_test_dish_id}}
@router.patch(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=200
)
async def patch_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        dish: schemas.UpdateDishes,
        db: Session = Depends(get_db),
):
    # check menu | submenu | dish
    _ = dish_get(menu_id, submenu_id, dish_id, db)

    db_dish = crud_dishes.update(dish_id, dish, db=db)
    return jsonable_encoder(db_dish, custom_encoder={float: str})


# DELETE /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes/{{api_test_dish_id}}
@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def delete_dish(
        menu_id: UUID, submenu_id: UUID, dish_id: UUID, db: Session = Depends(get_db)
):
    # check menu | submenu | dish
    _ = dish_get(menu_id, submenu_id, dish_id, db)

    try:
        crud_dishes.delete(dish_id, db=db)
    except Exception as e:
        raise HTTPException(status_code=e.args[0], detail=e.args[1])
    return
