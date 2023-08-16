import http
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.encoders import jsonable_encoder

from app.src import schemas
from app.src.services import DishesService

from .utils import cache, invalidate_cache

router = APIRouter()

DISH_PRICE_ENCODER = {float: lambda x: f'{round(float(x), 2):.2f}'}


@router.get(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    summary='Get all dishes from a submenu',
    status_code=http.HTTPStatus.OK,
)
@cache
async def get_dishes(
        menu_id: UUID,
        submenu_id: UUID,
        service: DishesService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    # TODO check submenu? 2 jsonable_encoder (((
    res = jsonable_encoder(await service.get_all(menu_id, submenu_id))
    return jsonable_encoder(res, custom_encoder=DISH_PRICE_ENCODER)


@router.get(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    summary='Get the dish by and id',
    status_code=http.HTTPStatus.OK,
)
@cache
async def get_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        service: DishesService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    res = jsonable_encoder(await service.get(menu_id, submenu_id, dish_id))
    return jsonable_encoder(res,
                            custom_encoder=DISH_PRICE_ENCODER)


@router.post(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    summary='Create the dish',
    status_code=http.HTTPStatus.CREATED,
)
@invalidate_cache
async def create_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish: schemas.CreateDishIn,
        service: DishesService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return jsonable_encoder(await service.create(menu_id, submenu_id, dish),
                            custom_encoder=DISH_PRICE_ENCODER)


@router.patch(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    summary='Update the dish',
    status_code=http.HTTPStatus.OK,
)
@invalidate_cache
async def patch_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        dish: schemas.UpdateDishIn,
        service: DishesService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return jsonable_encoder(await service.update(menu_id, submenu_id, dish_id, dish),
                            custom_encoder=DISH_PRICE_ENCODER)


@router.delete(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    summary='Delete the dish',
    status_code=http.HTTPStatus.OK,
)
@invalidate_cache
async def delete_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        service: DishesService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.delete(menu_id, submenu_id, dish_id)
