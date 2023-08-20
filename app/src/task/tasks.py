import asyncio

from app.src import crud
from app.src.config import TypeEnum, settings
from app.src.database import AsyncSession, async_session, ping_db
from app.src.repos import DishesRepository, MenuRepository, SubMenuRepository
from app.src.services.xls_menu import XlsMenuService

from .conn import app_celery


def get_xls_menu_service(session: AsyncSession) -> XlsMenuService | None:
    crud_menu = crud.MenusCRUD(session)
    repo_menus = MenuRepository(crud_menu)

    crud_submenu = crud.SubMenusCRUD(session)
    repo_submenus = SubMenuRepository(crud_submenu, repo_menus)

    crud_dishes = crud.DishesCRUD(session)
    repo_dishes = DishesRepository(crud_dishes, repo_menus, repo_submenus)
    return XlsMenuService(
        repo_menus=repo_menus,
        repo_submenus=repo_submenus,
        repo_dishes=repo_dishes)


async def async_xls_load():
    session: AsyncSession = async_session()
    if not (await ping_db(session)):
        print("can't load data")  # TODO write to log
        return

    service = get_xls_menu_service(session)
    await service.load_from_file(settings.EXCHANGE_FILE)
    await session.close()


async def async_xls_sheet_load():
    session: AsyncSession = async_session()
    if not (await ping_db(session)):
        print("can't load data")  # TODO write to log
        return

    service = get_xls_menu_service(session)
    await service.load_from_sheet(settings.EXCHANGE_SHEET_ID)
    await session.close()


@app_celery.task
def xls_load():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_xls_load())


@app_celery.task
def xls_sheet_load():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_xls_sheet_load())


@app_celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    if settings.EXCHANGE_TYPE == TypeEnum.file:
        sender.add_periodic_task(settings.EXCHANGE_SCHEDULE,
                                 xls_load.s(),
                                 name=f'sync file {settings.EXCHANGE_FILE} every {settings.EXCHANGE_SCHEDULE} sec')
    elif settings.EXCHANGE_TYPE == TypeEnum.sheet:
        sender.add_periodic_task(settings.EXCHANGE_SCHEDULE,
                                 xls_sheet_load.s(),
                                 name=f'sync with sheet {settings.EXCHANGE_SHEET_ID} every {settings.EXCHANGE_SCHEDULE} sec')
    else:
        print('param error')    # TODO write log
