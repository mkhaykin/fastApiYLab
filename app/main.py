import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.database import create_tables, get_db
from app.src.routes.dishes import router as dishes_router
from app.src.routes.menus import router as menu_router
from app.src.routes.submenus import router as submenu_router

create_tables()

app = FastAPI()

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dishes_router)


@app.get('/')
async def hello():
    return {'msg': 'Hello World'}


@app.get('/all')
async def orm_query(session: AsyncSession = Depends(get_db)):
    from sqlalchemy import func, select

    from app.src import models

    submenus_count = (
        select(
            models.SubMenus.menu_id,
            func.count(models.SubMenus.id).label('submenus_count'),
        )
        .group_by(models.SubMenus.menu_id)
        .subquery()
    )

    dishes_count = (
        select(
            models.SubMenus.menu_id,
            func.count(models.Dishes.id).label('dishes_count'),
        )
        .outerjoin(models.Dishes, models.Dishes.submenu_id == models.SubMenus.id)
        .group_by(models.SubMenus.menu_id)
        .subquery()
    )

    dishes_in_submenu_count = (
        select(
            models.SubMenus.id,
            func.count(models.Dishes.id).label('dishes_in_submenu_count'),
        )
        .outerjoin(models.Dishes, models.Dishes.submenu_id == models.SubMenus.id)
        .group_by(models.SubMenus.id)
        .subquery()
    )

    query = (
        select(
            models.Menus.id.label('menu_id'),
            models.Menus.title.label('menu_title'),
            models.Menus.description.label('menu_description'),
            submenus_count.c.submenus_count.label('menu_submenus_count'),
            dishes_count.c.dishes_count.label('menu_dishes_count'),
            models.SubMenus.id.label('submenu_id'),
            models.SubMenus.title.label('submenu_title'),
            models.SubMenus.description.label('submenu_description'),
            dishes_in_submenu_count.c.dishes_in_submenu_count.label('dishes_in_submenu_count'),
            models.Dishes.id.label('dish_id'),
            models.Dishes.title.label('dish_title'),
            models.Dishes.description.label('dish_description'),
        )
        .outerjoin(models.SubMenus, models.Menus.id == models.SubMenus.menu_id)
        .outerjoin(models.Dishes, models.SubMenus.id == models.Dishes.submenu_id)
        .outerjoin(submenus_count, submenus_count.c.menu_id == models.Menus.id)
        .outerjoin(dishes_count, dishes_count.c.menu_id == models.Menus.id)
        .outerjoin(dishes_in_submenu_count, dishes_in_submenu_count.c.id == models.SubMenus.id)

    )
    result = await session.execute(query)
    return result.mappings().all()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
