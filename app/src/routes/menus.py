from uuid import UUID

from fastapi import APIRouter, Depends

from app.src import schemas
from app.src.services import MenusService

router = APIRouter()


# GET /app/v1/menus
@router.get('/api/v1/menus')
async def get_menus(service: MenusService = Depends()):
    return await service.get_all()


# GET /app/v1/menus/{{api_test_menu_id}}
@router.get('/api/v1/menus/{menu_id}')
async def get_menu(menu_id: UUID, service: MenusService = Depends()):
    return await service.get(menu_id)


# POST /app/v1/menus
@router.post('/api/v1/menus', status_code=201)
async def create_menu(menu: schemas.CreateMenu, service: MenusService = Depends()):
    return await service.create(menu)


# PATCH /app/v1/menus/{{api_test_menu_id}}
@router.patch('/api/v1/menus/{menu_id}', status_code=200)
async def update_menu(
    menu_id: UUID, menu: schemas.UpdateMenu, service: MenusService = Depends()
):
    return await service.update(menu_id, menu)


# /app/v1/menus/{{api_test_menu_id}}
@router.delete('/api/v1/menus/{menu_id}')
async def delete_menu(menu_id: UUID, service: MenusService = Depends()):
    return await service.delete(menu_id)
