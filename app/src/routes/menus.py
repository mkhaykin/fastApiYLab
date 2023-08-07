import http
from uuid import UUID

from fastapi import APIRouter, Depends

from app.src import schemas
from app.src.services import MenusService

router = APIRouter()


# GET /app/v1/menus
@router.get('/api/v1/menus',
            summary='Get all menus',
            status_code=http.HTTPStatus.OK)
async def get_menus(service: MenusService = Depends()):
    return await service.get_all()


# GET /app/v1/menus/{{api_test_menu_id}}
@router.get('/api/v1/menus/{menu_id}',
            summary='Get one menu by an id',
            status_code=http.HTTPStatus.OK)
async def get_menu(menu_id: UUID, service: MenusService = Depends()):
    return await service.get(menu_id)


# POST /app/v1/menus
@router.post(path='/api/v1/menus',
             summary='Create the menu',
             status_code=http.HTTPStatus.CREATED)
async def create_menu(menu: schemas.CreateMenu, service: MenusService = Depends()):
    return await service.create(menu)


# PATCH /app/v1/menus/{{api_test_menu_id}}
@router.patch('/api/v1/menus/{menu_id}',
              summary='Update the menu',
              status_code=http.HTTPStatus.OK)
async def update_menu(
        menu_id: UUID, menu: schemas.UpdateMenu, service: MenusService = Depends()
):
    return await service.update(menu_id, menu)


# /app/v1/menus/{{api_test_menu_id}}
@router.delete('/api/v1/menus/{menu_id}',
               summary='Delete the menu',
               status_code=http.HTTPStatus.OK)
async def delete_menu(menu_id: UUID, service: MenusService = Depends()):
    return await service.delete(menu_id)
