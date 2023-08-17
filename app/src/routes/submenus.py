import http
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends

from app.src import schemas
from app.src.services import SubMenusService

from .utils import cache, invalidate_cache

router = APIRouter()


@router.get(
    path='/api/v1/menus/{menu_id}/submenus',
    summary='Get all submenus from a menu',
    status_code=http.HTTPStatus.OK,
    responses={404: {'model': schemas.MessageMenuNotFound, 'description': 'The menu was not found'}, },
    response_model=list[schemas.GetSubMenu],
    response_description='Return all menus',
)
@cache
async def get_submenus(
        menu_id: UUID,
        service: SubMenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.get_all(menu_id)


@router.get(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    summary='Get the submenu by an id',
    status_code=http.HTTPStatus.OK,
    responses={404: {'model': schemas.MessageSubMenuNotFound | schemas.MessageMenuNotFound,
                     'description': 'The menu | submenu was not found'}, },
    response_model=schemas.GetSubMenu,
    response_description='Return one menu by an id',
)
@cache
async def get_submenu(
        menu_id: UUID,
        submenu_id: UUID,
        service: SubMenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.get(menu_id, submenu_id)


@router.get(
    path='/api/v1/menus/{menu_id}/full',
    summary='Get all submenus with linked elements',
    status_code=http.HTTPStatus.OK,
    response_model=list[schemas.GetSubMenuFull],
    response_description='Return all submenus with linked elements',
)
async def get_submenus_full(
        menu_id: UUID,
        service: SubMenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.get_full(menu_id)


@router.post(
    path='/api/v1/menus/{menu_id}/submenus',
    summary='Create the submenu',
    status_code=http.HTTPStatus.CREATED,
    responses={404: {'model': schemas.MessageSubMenuNotFound | schemas.MessageMenuNotFound,
                     'description': 'The menu | submenu was not found'},
               409: {'model': schemas.MessageSubMenuDuplicated,
                     'description': 'The submenu with the title already exists'}, },
    response_model=schemas.CreateSubMenuOut,
    response_description='Return created submenu',
)
@invalidate_cache
async def create_submenu(
        menu_id: UUID,
        submenu: schemas.CreateSubMenuIn,
        service: SubMenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.create(menu_id, submenu)


@router.patch(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    summary='Update the submenu',
    status_code=http.HTTPStatus.OK,
    responses={404: {'model': schemas.MessageSubMenuNotFound | schemas.MessageMenuNotFound,
                     'description': 'The menu | submenu was not found'},
               409: {'model': schemas.MessageSubMenuDuplicated,
                     'description': 'The submenu with the title already exists'}, },
    response_model=schemas.UpdateSubMenuOut,
    response_description='Return created submenu',

)
@invalidate_cache
async def patch_submenu(
        menu_id: UUID,
        submenu_id: UUID,
        submenu: schemas.UpdateSubMenuIn,
        service: SubMenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.update(menu_id, submenu_id, submenu)


@router.delete(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    summary='Delete the submenu',
    status_code=http.HTTPStatus.OK,
    responses={404: {'model': schemas.MessageSubMenuNotFound | schemas.MessageMenuNotFound,
                     'description': 'The menu | submenu was not found'}, },
    response_model=schemas.MessageSubMenuDeleted,
    response_description='Return a confirm',
)
@invalidate_cache
async def delete_submenu(
        menu_id: UUID,
        submenu_id: UUID,
        service: SubMenusService = Depends(),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return await service.delete(menu_id, submenu_id)
