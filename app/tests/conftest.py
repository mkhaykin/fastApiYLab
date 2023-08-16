import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy_utils.functions import create_database, database_exists, drop_database

from app.main import app
from app.src.database import get_db
from app.src.models import Dishes, Menus, SubMenus
from app.tests.database import (
    SQLALCHEMY_DATABASE_TEST_URL,
    TestingSession,
    create_tables_async,
    drop_tables_async,
    engine_test_async,
    override_get_db,
)

# from app.src.cache.actions import cache_reset
from .utils_cache import cache_reset


@pytest_asyncio.fixture(scope='module')
async def db_prod() -> AsyncGenerator:
    app.dependency_overrides[get_db] = get_db
    yield TestingSession()


@pytest.fixture(scope='session')
def create_db():
    if not database_exists(SQLALCHEMY_DATABASE_TEST_URL):
        create_database(SQLALCHEMY_DATABASE_TEST_URL)
    yield
    drop_database(SQLALCHEMY_DATABASE_TEST_URL)


# drop all database every time when test complete
@pytest_asyncio.fixture(scope='module')
async def async_db_engine(create_db):
    app.dependency_overrides[get_db] = override_get_db
    await drop_tables_async()
    await create_tables_async()
    await cache_reset()

    yield engine_test_async


# truncate all table to isolate tests
@pytest_asyncio.fixture(scope='module')
async def async_db(async_db_engine):
    async with TestingSession() as session:
        yield session


@pytest_asyncio.fixture(scope='module')
async def async_client() -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url='http://test') as client:
            yield client


# let test session to know it is running inside event loop
@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


# @pytest_asyncio.fixture(scope='module')
# async def db_test() -> AsyncGenerator:
#     app.dependency_overrides[get_db] = override_get_db
#     await drop_tables_async()
#     await create_tables_async()
#     yield


@pytest_asyncio.fixture  # (scope='module')
async def client() -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url='http://test') as client:
            yield client


@pytest_asyncio.fixture(scope='module')
async def db_create_menus(async_db):
    async_db.add(
        Menus(
            id='00000000-0001-0000-0000-000000000000',
            title='Menu 1 title',
            description='Menu 1 description',
        )
    )
    async_db.add(
        Menus(
            id='00000000-0002-0000-0000-000000000000',
            title='Menu 2 title',
            description='Menu 2 description',
        )
    )
    await async_db.commit()
    yield async_db


@pytest_asyncio.fixture(scope='module')
async def db_create_submenus(db_create_menus):
    db_create_menus.add(
        SubMenus(
            id='00000000-0000-0001-0000-000000000000',
            menu_id='00000000-0001-0000-0000-000000000000',
            title='SubMenu 1 title',
            description='SubMenu 11 description',
        )
    )
    db_create_menus.add(
        SubMenus(
            id='00000000-0000-0002-0000-000000000000',
            menu_id='00000000-0001-0000-0000-000000000000',
            title='SubMenu 2 title',
            description='SubMenu 12 description',
        )
    )
    db_create_menus.add(
        SubMenus(
            id='00000000-0000-0003-0000-000000000000',
            menu_id='00000000-0002-0000-0000-000000000000',
            title='SubMenu 3 title',
            description='SubMenu 21 description',
        )
    )
    await db_create_menus.commit()
    yield db_create_menus


@pytest_asyncio.fixture(scope='module')
async def db_create_dishes(db_create_submenus):
    db_create_submenus.add(
        Dishes(
            id='00000000-0000-0000-0001-000000000000',
            submenu_id='00000000-0000-0001-0000-000000000000',
            title='Dish 1 title',
            description='Dish 1 description',
            price=10.0,
        )
    )
    db_create_submenus.add(
        Dishes(
            id='00000000-0000-0000-0002-000000000000',
            submenu_id='00000000-0000-0001-0000-000000000000',
            title='Dish 2 title',
            description='Dish 2 description',
            price=10.0,
        )
    )
    db_create_submenus.add(
        Dishes(
            id='00000000-0000-0000-0003-000000000000',
            submenu_id='00000000-0000-0002-0000-000000000000',
            title='Dish 3 title',
            description='Dish 3 description',
            price=10.0,
        )
    )
    await db_create_submenus.commit()
    yield db_create_submenus


@pytest_asyncio.fixture(scope='function')
async def db_create_dishes_clear_cache(db_create_dishes):
    await cache_reset()
    yield db_create_dishes
