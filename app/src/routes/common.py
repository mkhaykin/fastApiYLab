from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.src.crud import crud_menus, crud_submenus, crud_dishes


def menu_get(menu_id: UUID, db: Session):
    db_menu = crud_menus.get(menu_id, db=db)
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_menu


def submenu_get(menu_id: UUID, submenu_id: UUID, db: Session):
    # check menu
    _ = menu_get(menu_id, db)

    db_submenu = crud_submenus.get(submenu_id, db=db)
    if not db_submenu or db_submenu.menu_id != menu_id:
        raise HTTPException(status_code=404, detail="submenu not found")
    return db_submenu


def dish_get(menu_id: UUID, submenu_id: UUID, dish_id: UUID, db: Session):
    # check submenu
    _ = submenu_get(menu_id, submenu_id, db)

    db_dish = crud_dishes.get(dish_id, db=db)
    if not db_dish or db_dish.submenu_id != submenu_id:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish
