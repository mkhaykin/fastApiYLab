import http

from fastapi import APIRouter, Depends

from app.src import schemas
from app.src.config import settings
from app.src.services import XlsMenuService

router = APIRouter()


@router.get(
    path='/api/v1/file',
    summary='Sync data with /admin/Menu.xlsx',
    status_code=http.HTTPStatus.OK,
    response_model=schemas.MessageMenuLoad,
)
async def load_file(service: XlsMenuService = Depends()):
    return await service.load_from_file(settings.EXCHANGE_FILE)


@router.get(
    path='/api/v1/sheet',
    summary='Sync data with Google sheet',
    status_code=http.HTTPStatus.OK,
    response_model=schemas.MessageMenuLoad,
)
async def load_sheet(service: XlsMenuService = Depends()):
    return await service.load_from_sheet(settings.EXCHANGE_SHEET_ID)
