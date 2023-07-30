import pytest
from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import drop_database

from app.main import app
from app.src.database import Base
from app.src.database import get_db

from app.src.models import Menus
from app.src.models import SubMenus
from app.src.models import Dishes

from app.tests.database import engine as engine_test
from app.tests.database import override_get_db
from app.tests.database import SQLALCHEMY_DATABASE_URL
from app.tests.database import TestingSession


@pytest.fixture(scope="session")
def create_test_db() -> Generator:
    if not database_exists(SQLALCHEMY_DATABASE_URL):
        create_database(SQLALCHEMY_DATABASE_URL)
    yield TestingSession()
    drop_database(SQLALCHEMY_DATABASE_URL)


@pytest.fixture(scope="module")
def db_test(create_test_db) -> Generator:
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    yield create_test_db


@pytest.fixture(scope="module")
def db_prod() -> Generator:
    app.dependency_overrides[get_db] = get_db
    yield TestingSession()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def db_create_menus(db_test):
    db_test.add(
        Menus(
            id="00000000-0000-0000-0000-000000000000",
            title="Menu 1 title",
            description="Menu 1 description",
        )
    )
    db_test.add(
        Menus(
            id="00000000-0000-0000-0000-000000000001",
            title="Menu 2 title",
            description="Menu 2 description",
        )
    )
    db_test.commit()
    yield db_test


@pytest.fixture(scope="module")
def db_create_submenus(db_create_menus):
    db_create_menus.add(
        SubMenus(
            id="00000000-0000-0000-0000-000000000000",
            menu_id="00000000-0000-0000-0000-000000000000",
            title="SubMenu 1 title",
            description="SubMenu 1 description",
        )
    )
    db_create_menus.add(
        SubMenus(
            id="00000000-0000-0000-0000-000000000001",
            menu_id="00000000-0000-0000-0000-000000000000",
            title="SubMenu 2 title",
            description="SubMenu 2 description",
        )
    )
    db_create_menus.add(
        SubMenus(
            id="00000000-0000-0000-0000-000000000002",
            menu_id="00000000-0000-0000-0000-000000000001",
            title="SubMenu 3 title",
            description="SubMenu 3 description",
        )
    )
    db_create_menus.commit()
    yield db_create_menus


@pytest.fixture(scope="module")
def db_create_dishes(db_create_submenus):
    db_create_submenus.add(
        Dishes(
            id="00000000-0000-0000-0000-000000000000",
            submenu_id="00000000-0000-0000-0000-000000000000",
            title="Dish 1 title",
            description="Dish 1 description",
            price=10.0,
        )
    )
    db_create_submenus.add(
        Dishes(
            id="00000000-0000-0000-0000-000000000001",
            submenu_id="00000000-0000-0000-0000-000000000000",
            title="Dish 2 title",
            description="Dish 2 description",
            price=10.0,
        )
    )
    db_create_submenus.add(
        Dishes(
            id="00000000-0000-0000-0000-000000000002",
            submenu_id="00000000-0000-0000-0000-000000000001",
            title="Dish 3 title",
            description="Dish 3 description",
            price=10.0,
        )
    )
    db_create_submenus.commit()
    yield db_create_submenus
