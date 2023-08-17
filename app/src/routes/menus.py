import http
import os
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends

from app.src import schemas
from app.src.config import settings
from app.src.services import MenusService, XlsMenuService

from .utils import cache, invalidate_cache

router = APIRouter()


@router.get(
    path='/api/v1/menus/load',
    summary='Sync data with /admin/Menu.xlsx',
    status_code=http.HTTPStatus.OK,
    response_model=schemas.MessageMenuLoad,
)
async def read_main(service: XlsMenuService = Depends()):
    filename: str = os.path.join(settings.PATH_TO_STORE, 'Menu.xlsx')
    await service.load_from_file(filename)
    return {'msg': 'data loads slow'}


@router.get(
    path='/api/v1/menus',
    summary='Get all menus',
    status_code=http.HTTPStatus.OK,
    response_model=list[schemas.GetMenu],
    response_description='Return all menus',
)
@cache
async def get_menus(
        service: MenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.get_all()


@router.get(
    path='/api/v1/menus/{menu_id}',
    summary='Get a menu',
    status_code=http.HTTPStatus.OK,
    responses={404: {'model': schemas.MessageMenuNotFound, 'description': 'The menu was not found'}, },
    response_model=schemas.GetMenu,
    response_description='Return one menu by an id',
)
@cache
async def get_menu(
        menu_id: UUID,
        service: MenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.get(menu_id)


@router.get(
    path='/api/v1/menus/full',
    summary='Get all menus with linked elements',
    status_code=http.HTTPStatus.OK,
    response_model=list[schemas.GetMenuFull],
    response_description='Return all menus with linked elements',
)
async def get_menus_full(
        service: MenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.get_full()


@router.post(
    path='/api/v1/menus',
    summary='Create the menu',
    status_code=http.HTTPStatus.CREATED,
    responses={404: {'model': schemas.MessageMenuNotFound, 'description': 'The menu was not found'},
               409: {'model': schemas.MessageMenuDuplicated,
                     'description': 'The menu with the title already exists'}, },
    response_model=schemas.CreateMenuOut,
    response_description='Return created menu',
)
@invalidate_cache
async def create_menu(
        menu: schemas.CreateMenuIn,
        service: MenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.create(menu)


@router.patch(
    path='/api/v1/menus/{menu_id}',
    summary='Update the menu',
    status_code=http.HTTPStatus.OK,
    responses={404: {'model': schemas.MessageMenuNotFound, 'description': 'The menu was not found'},
               409: {'model': schemas.MessageMenuDuplicated,
                     'description': 'The menu with the title already exists'}, },
    response_model=schemas.UpdateMenuOut,
    response_description='Return updated menu',
)
@invalidate_cache
async def update_menu(
        menu_id: UUID,
        menu: schemas.UpdateMenuIn,
        service: MenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.update(menu_id, menu)


@router.delete(
    path='/api/v1/menus/{menu_id}',
    summary='Delete the menu',
    status_code=http.HTTPStatus.OK,
    responses={404: {'model': schemas.MessageMenuNotFound, 'description': 'The menu was not found'}, },
    response_model=schemas.MessageMenuDeleted,
    response_description='Return a confirm',
)
@invalidate_cache
async def delete_menu(
        menu_id: UUID,
        service: MenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.delete(menu_id)
