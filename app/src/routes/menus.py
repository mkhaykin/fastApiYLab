import http
import os
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends

from app.src import schemas
from app.src.config import settings
from app.src.services import MenusService, XlsMenuService

from .utils import cache, invalidate_cache

router = APIRouter()


@router.get('/api/v1/menus/load')
async def read_main(service: XlsMenuService = Depends()):
    filename: str = os.path.join(settings.PATH_TO_STORE, 'Menu.xlsx')
    await service.load_from_file(filename)
    return {'msg': 'data loads slow'}


@router.get(
    path='/api/v1/menus',
    summary='Get all menus',
    status_code=http.HTTPStatus.OK
)
@cache
async def get_menus(
        service: MenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.get_all()


@router.get(
    path='/api/v1/menus/{menu_id}',
    summary='Get one menu by an id',
    status_code=http.HTTPStatus.OK,
)
@cache
async def get_menu(
        menu_id: UUID,
        service: MenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.get(menu_id)


@router.get(
    path='/api/v1/full',
    summary='Get all menus with linked elements',
    status_code=http.HTTPStatus.OK
)
async def get_menus_full(
        service: MenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.get_full()


@router.post(
    path='/api/v1/menus',
    summary='Create the menu',
    status_code=http.HTTPStatus.CREATED
)
@invalidate_cache
async def create_menu(
        menu: schemas.CreateMenuIn,
        service: MenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    result = await service.create(menu)
    return result


@router.patch(
    path='/api/v1/menus/{menu_id}',
    summary='Update the menu',
    status_code=http.HTTPStatus.OK
)
@invalidate_cache
async def update_menu(
        menu_id: UUID,
        menu: schemas.UpdateMenuIn,
        service: MenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    result = await service.update(menu_id, menu)
    return result


@router.delete(
    path='/api/v1/menus/{menu_id}',
    summary='Delete the menu',
    status_code=http.HTTPStatus.OK
)
@invalidate_cache
async def delete_menu(
        menu_id: UUID,
        service: MenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    await service.delete(menu_id)
    return
