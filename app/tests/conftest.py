import pytest
import os
from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import drop_database

from app.main import app
from app.src.database import Base
from app.src.database import get_db

from app.tests.database import engine as engine_test
from app.tests.database import override_get_db
from app.tests.database import SQLALCHEMY_DATABASE_URL
from app.tests.database import TestingSession


@pytest.fixture(scope="module")
def db_test() -> Generator:
    if not database_exists(SQLALCHEMY_DATABASE_URL):
        create_database(SQLALCHEMY_DATABASE_URL)

    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine_test)

    yield TestingSession()

    Base.metadata.drop_all(bind=engine_test)
    drop_database(SQLALCHEMY_DATABASE_URL)


@pytest.fixture(scope="module")
def db_prod() -> Generator:
    app.dependency_overrides[get_db] = get_db
    yield TestingSession()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
