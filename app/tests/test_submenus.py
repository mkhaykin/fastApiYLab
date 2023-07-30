"""
    на момент теста у нас 2 записи по меню
    00000000-0000-0000-0000-000000000000
    00000000-0000-0000-0000-000000000001
"""
from app.tests.utils import random_word


def test_menu_exist(db_create_menus, client):
    response = client.get(f"/api/v1/menus/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 200
    response = client.get(f"/api/v1/menus/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 200


def test_submenus(db_create_menus, client):
    response = client.get("/api/v1/menus/00000000-0000-0000-0000-000000000000/submenus")
    assert response.status_code == 200
    assert not response.json()


def test_submenu_not_found(db_create_menus, client):
    response = client.get(
        "/api/v1/menus/00000000-0000-0000-0000-000000000000/"
        + "submenus/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


def test_create_submenu_fix(db_create_menus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus",
        json={"title": "Submenu 1", "description": "Submenu 1 description"},
    )
    assert response.status_code == 201
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()

    submenu_id = response.json()["id"]
    assert response.json() == {
        "id": submenu_id,
        "menu_id": menu_id,
        "title": "Submenu 1",
        "description": "Submenu 1 description",
        "dishes_count": 0,
    }


def test_create_submenu_duplicate(db_create_menus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus",
        json={"title": "Submenu 1", "description": "Submenu 1 description"},
    )
    assert response.status_code == 409


def test_create_submenu_duplicate_another_submenu(db_create_menus, client):
    menu_id = "00000000-0000-0000-0000-000000000001"
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus",
        json={"title": "Submenu 1", "description": "Submenu 1 description"},
    )
    assert response.status_code == 409


def test_create_submenu_menu_not_exist(db_create_menus, client):
    menu_id = "00000000-0000-0000-0000-000000000002"
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus",
        json={"title": "Submenu ...", "description": "Submenu ... description"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}


def test_create_submenu(db_create_menus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    title = random_word(10)
    description = random_word(20)
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus",
        json={
            "title": f"{title}",
            "description": f"{description}",
        },
    )
    assert response.status_code == 201
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()

    submenu_id = response.json()["id"]
    assert response.json() == {
        "id": submenu_id,
        "menu_id": menu_id,
        "title": title,
        "description": description,
        "dishes_count": 0,
    }


def test_create_submenu_and_check(db_create_menus, client):
    menu_id = "00000000-0000-0000-0000-000000000001"
    # create
    title = random_word(11)
    description = random_word(20)
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus",
        json={
            "title": f"{title}",
            "description": f"{description}",
        },
    )
    assert response.status_code == 201
    submenu_id = response.json()["id"]

    # get submenu by id
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": submenu_id,
        "menu_id": menu_id,
        "title": title,
        "description": description,
        "dishes_count": 0,
    }

    # get all submenus
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/")
    assert response.status_code == 200
    assert response.json() and any(
        map(
            lambda item: item
            == {
                "id": submenu_id,
                "menu_id": menu_id,
                "title": title,
                "description": description,
                "dishes_count": 0,
            },
            response.json(),
        )
    )


def test_update_submenu_and_check(db_create_menus, client):
    menu_id = "00000000-0000-0000-0000-000000000001"
    # create
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus",
        json={
            "title": f"{random_word(12)}",
            "description": f"{random_word(20)}",
        },
    )
    assert response.status_code == 201
    submenu_id = response.json()["id"]
    title = random_word(13)
    description = random_word(20)

    # patch
    response = client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
        json={
            "title": title,
            "description": description,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": submenu_id,
        "menu_id": menu_id,
        "title": title,
        "description": description,
        "dishes_count": 0,
    }

    # get submenu by id
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": submenu_id,
        "menu_id": menu_id,
        "title": title,
        "description": description,
        "dishes_count": 0,
    }

    # get all submenus
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/")
    assert response.status_code == 200
    assert response.json() and any(
        map(
            lambda item: item
            == {
                "id": submenu_id,
                "menu_id": menu_id,
                "title": title,
                "description": description,
                "dishes_count": 0,
            },
            response.json(),
        )
    )


def test_delete_submenu_and_check(db_create_menus, client):
    menu_id = "00000000-0000-0000-0000-000000000001"
    # create
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus",
        json={
            "title": f"{random_word(14)}",
            "description": f"{random_word(20)}",
        },
    )
    assert response.status_code == 201
    submenu_id = response.json()["id"]

    # delete
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200

    # get submenu by id
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 404

    # get all submenus
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/")
    assert response.status_code == 200
    assert not response.json() or not any(
        map(
            lambda item: item["id"] == submenu_id,
            response.json(),
        )
    )

    # check all menus!
    menus = client.get(f"/api/v1/menus/").json()
    for menu in menus:
        submenus = client.get(f"/api/v1/menus/{menu['id']}/submenus").json()
        assert not submenus or not any(
            map(
                lambda item: item["id"] == submenu_id,
                submenus,
            )
        )


def test_delete_submenu_not_exist(db_test, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    submenu_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 404
