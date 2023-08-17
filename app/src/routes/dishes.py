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
    response_model=list[schemas.GetDish],
    response_description='Return dishes by an menu_id and an submenu_id',
)
@cache
async def get_dishes(
        menu_id: UUID,
        submenu_id: UUID,
        service: DishesService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    # TODO check submenu? 2 jsonable_encoder (((
    # res = jsonable_encoder(await service.get_all(menu_id, submenu_id))
    # return jsonable_encoder(res, custom_encoder=DISH_PRICE_ENCODER)
    return await service.get_all(menu_id, submenu_id)


@router.get(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    summary='Get the dish by and id',
    status_code=http.HTTPStatus.OK,
    responses={
        404: {'model': schemas.MessageDishNotFound | schemas.MessageSubMenuNotFound | schemas.MessageMenuNotFound,
              'description': 'The menu | submenu | dish was not found'},
    },
    response_model=schemas.GetDish,
    response_description='Return one dish',
)
@cache
async def get_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        service: DishesService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    # res = jsonable_encoder(await service.get(menu_id, submenu_id, dish_id))
    # return jsonable_encoder(res,
    #                         custom_encoder=DISH_PRICE_ENCODER)
    return await service.get(menu_id, submenu_id, dish_id)


@router.post(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    summary='Create the dish',
    status_code=http.HTTPStatus.CREATED,
    responses={
        404: {'model': schemas.MessageSubMenuNotFound | schemas.MessageMenuNotFound,
              'description': 'The menu | submenu was not found'},
        409: {'model': schemas.MessageDishDuplicated,
              'description': 'The dish with the title already exists'},
    },
    response_model=schemas.CreateDishOut,
    response_description='Return created submenu',
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
    responses={
        404: {'model': schemas.MessageDishNotFound | schemas.MessageSubMenuNotFound | schemas.MessageMenuNotFound,
              'description': 'The menu | submenu | dish was not found'},
        409: {'model': schemas.MessageDishDuplicated,
              'description': 'The dish with the title already exists'},
    },
    response_model=schemas.UpdateDishOut,
    response_description='Return created submenu',
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
    # return jsonable_encoder(await service.update(menu_id, submenu_id, dish_id, dish),
    #                         custom_encoder=DISH_PRICE_ENCODER)
    return await service.update(menu_id, submenu_id, dish_id, dish)


@router.delete(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    summary='Delete the dish',
    status_code=http.HTTPStatus.OK,
    responses={
        404: {'model': schemas.MessageDishNotFound | schemas.MessageSubMenuNotFound | schemas.MessageMenuNotFound,
              'description': 'The menu | submenu | dish was not found'},
    },
    response_model=schemas.MessageDishDeleted,
    response_description='Return a confirm',
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
