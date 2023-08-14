import http
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends

from app.src import schemas
from app.src.cache import Cache, get_cache
from app.src.services import MenusService

router = APIRouter()


@router.get(
    path='/api/v1/menus',
    summary='Get all menus',
    status_code=http.HTTPStatus.OK
)
async def get_menus(
        service: MenusService = Depends()
):
    return await service.get_all()


@router.get(
    path='/api/v1/menus/{menu_id}',
    summary='Get one menu by an id',
    status_code=http.HTTPStatus.OK
)
async def get_menu(
        menu_id: UUID,
        service: MenusService = Depends()
):
    return await service.get(menu_id)


@router.get(
    path='/api/v1/full',
    summary='Get all menus with linked elements',
    status_code=http.HTTPStatus.OK
)
async def get_menus_full(
        service: MenusService = Depends()
):
    return await service.get_full()


@router.post(
    path='/api/v1/menus',
    summary='Create the menu',
    status_code=http.HTTPStatus.CREATED
)
async def create_menu(
        menu: schemas.CreateMenuIn,
        background_tasks: BackgroundTasks,
        service: MenusService = Depends(),
        cache: Cache = Depends(get_cache),
):
    background_tasks.add_task(cache.cache_del, 'menu:None:None', )
    return await service.create(menu)


@router.patch(
    path='/api/v1/menus/{menu_id}',
    summary='Update the menu',
    status_code=http.HTTPStatus.OK
)
async def update_menu(
        menu_id: UUID,
        menu: schemas.UpdateMenuIn,
        background_tasks: BackgroundTasks,
        service: MenusService = Depends(),
        cache: Cache = Depends(get_cache),
):
    background_tasks.add_task(cache.cache_del, 'menu:None:None')
    background_tasks.add_task(cache.cache_del_pattern, f'{menu_id}:*:*')
    return await service.update(menu_id, menu)


@router.delete(
    path='/api/v1/menus/{menu_id}',
    summary='Delete the menu',
    status_code=http.HTTPStatus.OK
)
async def delete_menu(
        menu_id: UUID,
        background_tasks: BackgroundTasks,
        service: MenusService = Depends(),
        cache: Cache = Depends(get_cache),
):
    background_tasks.add_task(cache.cache_del, 'menu:None:None')
    background_tasks.add_task(cache.cache_del_pattern, f'{menu_id}:*:*')
    return await service.delete(menu_id)
