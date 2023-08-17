import asyncio
import os

from app.src import crud
from app.src.config import settings
from app.src.database import AsyncSession, async_session, ping_db
from app.src.repos import DishesRepository, MenuRepository, SubMenuRepository
from app.src.services.xls_menu import XlsMenuService

from .conn import app_celery


async def async_xls_load():
    session: AsyncSession = async_session()
    if not (await ping_db(session)):
        print("can't load data")    # TODO write to log
        return

    filename: str = os.path.join(settings.PATH_TO_STORE, 'Menu.xlsx')
    crud_menu = crud.MenusCRUD(session)
    repo_menus = MenuRepository(crud_menu)

    crud_submenu = crud.SubMenusCRUD(session)
    repo_submenus = SubMenuRepository(crud_submenu, repo_menus)

    crud_dishes = crud.DishesCRUD(session)
    repo_dishes = DishesRepository(crud_dishes, repo_menus, repo_submenus)
    await (XlsMenuService(
        repo_menus=repo_menus,
        repo_submenus=repo_submenus,
        repo_dishes=repo_dishes)
        .load_from_file(filename))
    await session.close()


@app_celery.task
def xls_load():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_xls_load())


@app_celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls xls_load every 15 seconds.
    sender.add_periodic_task(15.0, xls_load.s(), name='sync file admin/Menu.xlsx every 15 sec')
