"""
    Тестирование прод базы.
    Только проверка api.
"""


def test_alive(client, db_prod):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_menus(client, db_prod):
    response = client.get("/api/v1/menus")
    assert response.status_code == 200


def test_submenus(client, db_prod):
    response = client.get("/api/v1/menus/00000000-0000-0000-0000-000000000000/submenus")
    assert response.status_code == 200


def test_dishes(client, db_prod):
    response = client.get(
        "/api/v1/menus/00000000-0000-0000-0000-000000000000/submenus/00000000-0000-0000-0000-000000000000/dishes"
    )
    assert response.status_code == 200
