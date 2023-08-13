import asyncio
import os

from app.src.cache import get_cache
from app.src.config import settings
from app.src.database import get_db
from app.src.services.xls_menu import XlsMenuService

from .conn import app_celery


async def async_xls_load():
    db = await anext(get_db())
    cache = await anext(get_cache())
    filename: str = os.path.join(settings.PATH_TO_STORE, 'Menu.xlsx')
    await XlsMenuService(db, cache).load_from_file(filename)


@app_celery.task
def xls_load():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_xls_load())


@app_celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls xls_load every 15 seconds.
    sender.add_periodic_task(15.0, xls_load.s(), name='sync file admin/Menu.xlsx every 15')
