import http
from uuid import UUID

from fastapi import APIRouter, Depends

from app.src import schemas
from app.src.services import SubMenusService

router = APIRouter()


# GET /app/v1/menus/{{api_test_menu_id}}/submenus
@router.get('/api/v1/menus/{menu_id}/submenus',
            summary='Get all submenus from a menu',
            status_code=http.HTTPStatus.OK)
async def get_submenus(menu_id: UUID, service: SubMenusService = Depends()):
    return await service.get_all(menu_id)


# GET /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}
@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}',
            summary='Get the submenu by an id',
            status_code=http.HTTPStatus.OK)
async def get_submenu(menu_id: UUID, submenu_id: UUID, service: SubMenusService = Depends()):
    return await service.get(menu_id, submenu_id)


# POST /app/v1/menus/{{api_test_menu_id}}/submenus
@router.post('/api/v1/menus/{menu_id}/submenus',
             summary='Create the submenu',
             status_code=http.HTTPStatus.CREATED)
async def create_submenu(
        menu_id: UUID, submenu: schemas.CreateSubMenuIn, service: SubMenusService = Depends()
):
    return await service.create(menu_id, submenu)


# PATCH /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}
@router.patch(path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
              summary='Update the submenu',
              status_code=http.HTTPStatus.OK)
async def patch_submenu(
        menu_id: UUID,
        submenu_id: UUID,
        submenu: schemas.UpdateSubMenuIn,
        service: SubMenusService = Depends(),
):
    return await service.update(menu_id, submenu_id, submenu)


# DELETE /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}
@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}',
               summary='Delete the submenu',
               status_code=http.HTTPStatus.OK)
async def delete_submenu(
        menu_id: UUID, submenu_id: UUID, service: SubMenusService = Depends()
):
    return await service.delete(menu_id, submenu_id)
