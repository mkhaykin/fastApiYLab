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
from app.tests.test_data import (
    DISH1,
    DISH2,
    DISH3,
    MENU1,
    MENU2,
    SUBMENU1,
    SUBMENU2,
    SUBMENU3,
)
from app.tests.test_utils_cache import cache_reset


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
@pytest_asyncio.fixture(scope='function')
async def async_db_engine(create_db):
    app.dependency_overrides[get_db] = override_get_db
    await drop_tables_async()
    await create_tables_async()
    await cache_reset()

    yield engine_test_async


@pytest_asyncio.fixture(scope='function')
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


@pytest_asyncio.fixture(scope='function')
async def db_test_data(async_db):
    async_db.add(Menus(**MENU1))
    async_db.add(Menus(**MENU2))
    await async_db.commit()
    async_db.add(SubMenus(**SUBMENU1))
    async_db.add(SubMenus(**SUBMENU2))
    async_db.add(SubMenus(**SUBMENU3))
    await async_db.commit()
    async_db.add(Dishes(**DISH1))
    async_db.add(Dishes(**DISH2))
    async_db.add(Dishes(**DISH3))
    await async_db.commit()

    await cache_reset()
    yield async_db
