"""
    Тестирование прод базы.
    Только проверка api.
"""
from sqlalchemy.orm.session import Session
from starlette.testclient import TestClient


def test_alive(db_prod: Session, client: TestClient):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello World'}


def test_menus(db_prod: Session, client: TestClient):
    response = client.get('/api/v1/menus')
    assert response.status_code == 200


def test_submenus(db_prod: Session, client: TestClient):
    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000/submenus')
    assert response.status_code == 200


def test_dishes(db_prod: Session, client: TestClient):
    response = client.get(
        '/api/v1/menus/00000000-0000-0000-0000-000000000000/submenus/00000000-0000-0000-0000-000000000000/dishes'
    )
    assert response.status_code == 200
