import http
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends

from app.src import schemas
from app.src.cache import Cache, get_cache
from app.src.services import SubMenusService

router = APIRouter()


@router.get(
    path='/api/v1/menus/{menu_id}/submenus',
    summary='Get all submenus from a menu',
    status_code=http.HTTPStatus.OK
)
async def get_submenus(
        menu_id: UUID,
        service: SubMenusService = Depends()
):
    return await service.get_all(menu_id)


@router.get(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    summary='Get the submenu by an id',
    status_code=http.HTTPStatus.OK
)
async def get_submenu(
        menu_id: UUID,
        submenu_id: UUID,
        service: SubMenusService = Depends()
):
    return await service.get(menu_id, submenu_id)


@router.get(
    path='/api/v1/menus/{menu_id}/full',
    summary='Get all menus with linked elements',
    status_code=http.HTTPStatus.OK
)
async def get_submenus_full(
        menu_id: UUID,
        service: SubMenusService = Depends()):
    return await service.get_full(menu_id)


@router.post(
    path='/api/v1/menus/{menu_id}/submenus',
    summary='Create the submenu',
    status_code=http.HTTPStatus.CREATED
)
async def create_submenu(
        menu_id: UUID,
        submenu: schemas.CreateSubMenuIn,
        background_tasks: BackgroundTasks,
        service: SubMenusService = Depends(),
        cache: Cache = Depends(get_cache),
):
    background_tasks.add_task(cache.cache_del_pattern, f'{menu_id}:*:*')
    return await service.create(menu_id, submenu)


@router.patch(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    summary='Update the submenu',
    status_code=http.HTTPStatus.OK
)
async def patch_submenu(
        menu_id: UUID,
        submenu_id: UUID,
        submenu: schemas.UpdateSubMenuIn,
        background_tasks: BackgroundTasks,
        service: SubMenusService = Depends(),
        cache: Cache = Depends(get_cache),
):
    background_tasks.add_task(cache.cache_del_pattern, f'*:{submenu_id}:*')
    return await service.update(menu_id, submenu_id, submenu)


@router.delete(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    summary='Delete the submenu',
    status_code=http.HTTPStatus.OK
)
async def delete_submenu(
        menu_id: UUID,
        submenu_id: UUID,
        background_tasks: BackgroundTasks,
        service: SubMenusService = Depends(),
        cache: Cache = Depends(get_cache),
):
    background_tasks.add_task(cache.cache_del_pattern, f'{menu_id}:*:*')
    return await service.delete(menu_id, submenu_id)
