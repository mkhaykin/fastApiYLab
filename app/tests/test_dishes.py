"""
    на момент теста у нас 2 записи по меню и 3 записи submenu
    00000000-0000-0000-0000-000000000000
        00000000-0000-0000-0000-000000000000
        00000000-0000-0000-0000-000000000001
    00000000-0000-0000-0000-000000000001
        00000000-0000-0000-0000-000000000002
"""
from app.tests.utils import random_word


def test_menu_exist(db_create_submenus, client):
    response = client.get("/api/v1/menus/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 200
    response = client.get("/api/v1/menus/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 200


def test_submenu_exist(db_create_submenus, client):
    response = client.get(
        "/api/v1/menus/00000000-0000-0000-0000-000000000000/"
        + "submenus/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 200
    response = client.get(
        "/api/v1/menus/00000000-0000-0000-0000-000000000000/"
        + "submenus/00000000-0000-0000-0000-000000000001"
    )
    assert response.status_code == 200
    response = client.get(
        "/api/v1/menus/00000000-0000-0000-0000-000000000001/"
        + "submenus/00000000-0000-0000-0000-000000000002"
    )
    assert response.status_code == 200


def test_dishes(db_create_submenus, client):
    response = client.get(
        "/api/v1/menus/00000000-0000-0000-0000-000000000000/"
        + "submenus/00000000-0000-0000-0000-000000000000/"
        + "dishes"
    )
    assert response.status_code == 200
    assert not response.json()


def test_dishes_not_found(db_create_submenus, client):
    response = client.get(
        "/api/v1/menus/00000000-0000-0000-0000-000000000000/"
        + "submenus/00000000-0000-0000-0000-000000000000/"
        + "dishes/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}


def test_dishes_not_found_wrong_submenu(db_create_submenus, client):
    response = client.get(
        "/api/v1/menus/00000000-0000-0000-0000-000000000000/"
        + "submenus/00000000-0000-0000-0000-000000000002/"
        + "dishes/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


def test_create_dishes_fix(db_create_submenus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    submenu_id = "00000000-0000-0000-0000-000000000000"
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={"title": "Dishes 1", "description": "Dishes 1 description", "price": "1"},
    )
    assert response.status_code == 201
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()

    dishes_id = response.json()["id"]
    assert response.json() == {
        "id": dishes_id,
        "submenu_id": submenu_id,
        "title": "Dishes 1",
        "description": "Dishes 1 description",
        "price": "1.0",
    }


def test_create_dish_duplicate(db_create_submenus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    submenu_id = "00000000-0000-0000-0000-000000000000"
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": "Dishes 1",
            "description": "Dishes 1 description",
            "price": "1",
        },
    )
    assert response.status_code == 409


def test_create_dish_duplicate_another_submenu(db_create_submenus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    submenu_id = "00000000-0000-0000-0000-000000000001"
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": "Dishes 1",
            "description": "Dishes 1 description",
            "price": "1",
        },
    )
    assert response.status_code == 409


def test_create_dish_duplicate_another_menu(db_create_submenus, client):
    menu_id = "00000000-0000-0000-0000-000000000001"
    submenu_id = "00000000-0000-0000-0000-000000000000"
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": "Dishes 1",
            "description": "Dishes 1 description",
            "price": "1",
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


def test_create_dish_submenu_not_exist(db_create_submenus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    submenu_id = "00000000-0000-0000-0000-000000000002"
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": "Dishes ...",
            "description": "Dishes ... description",
            "price": "1",
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


def test_create_dish_menu_not_exist(db_create_submenus, client):
    menu_id = "00000000-0000-0000-0000-000000000003"
    submenu_id = "00000000-0000-0000-0000-000000000001"
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": "Dishes ...",
            "description": "Dishes ... description",
            "price": "1",
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}


def test_create_dish(db_create_submenus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    submenu_id = "00000000-0000-0000-0000-000000000000"
    title = random_word(10)
    description = random_word(20)
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": f"{title}",
            "description": f"{description}",
            "price": "1",
        },
    )
    assert response.status_code == 201
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert "price" in response.json()

    dish_id = response.json()["id"]
    assert response.json() == {
        "id": dish_id,
        "submenu_id": submenu_id,
        "title": title,
        "description": description,
        "price": "1.0",
    }


def test_create_dish_price_10_22(db_create_submenus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    submenu_id = "00000000-0000-0000-0000-000000000000"
    title = random_word(5)
    description = random_word(20)
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": f"{title}",
            "description": f"{description}",
            "price": "10.22",
        },
    )
    assert response.status_code == 201
    dish_id = response.json()["id"]
    assert response.json() == {
        "id": dish_id,
        "submenu_id": submenu_id,
        "title": title,
        "description": description,
        "price": "10.22",
    }


def test_create_dish_price_10_123(db_create_submenus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    submenu_id = "00000000-0000-0000-0000-000000000000"
    title = random_word(6)
    description = random_word(20)
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": f"{title}",
            "description": f"{description}",
            "price": "10.123",
        },
    )
    assert response.status_code == 201
    dish_id = response.json()["id"]
    assert response.json() == {
        "id": dish_id,
        "submenu_id": submenu_id,
        "title": title,
        "description": description,
        "price": "10.12",
    }


def test_create_dish_price_10_126(db_create_submenus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    submenu_id = "00000000-0000-0000-0000-000000000000"
    title = random_word(7)
    description = random_word(20)
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": f"{title}",
            "description": f"{description}",
            "price": "10.126",
        },
    )
    assert response.status_code == 201
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert "price" in response.json()

    dish_id = response.json()["id"]
    assert response.json() == {
        "id": dish_id,
        "submenu_id": submenu_id,
        "title": title,
        "description": description,
        "price": "10.13",
    }


def test_create_dish_and_check(db_create_submenus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    submenu_id = "00000000-0000-0000-0000-000000000000"
    # create
    title = random_word(11)
    description = random_word(20)
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": f"{title}",
            "description": f"{description}",
            "price": "1",
        },
    )
    assert response.status_code == 201
    dish_id = response.json()["id"]

    # get dish by id
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": dish_id,
        "submenu_id": submenu_id,
        "title": title,
        "description": description,
        "price": "1.0",
    }

    # get all submenus
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    assert response.status_code == 200
    assert response.json() and any(
        map(
            lambda item: item
            == {
                "id": dish_id,
                "submenu_id": submenu_id,
                "title": title,
                "description": description,
                "price": "1.0",
            },
            response.json(),
        )
    )


def test_update_submenu_and_check(db_create_submenus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    submenu_id = "00000000-0000-0000-0000-000000000001"
    # create
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": f"{random_word(12)}",
            "description": f"{random_word(20)}",
            "price": "1",
        },
    )
    assert response.status_code == 201
    dish_id = response.json()["id"]
    title = random_word(13)
    description = random_word(20)

    # patch
    response = client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        json={"title": title, "description": description, "price": "1"},
    )
    answer = {
        "id": dish_id,
        "submenu_id": submenu_id,
        "title": title,
        "description": description,
        "price": "1.0",
    }
    assert response.status_code == 200
    assert response.json() == answer

    # get dish by id
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    )
    assert response.status_code == 200
    assert response.json() == answer

    # get all dish
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200
    assert response.json() and any(
        map(
            lambda item: item == answer,
            response.json(),
        )
    )


def test_delete_submenu_and_check(db_create_submenus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    submenu_id = "00000000-0000-0000-0000-000000000001"
    # create
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": f"{random_word(13)}",
            "description": f"{random_word(20)}",
            "price": "1",
        },
    )
    assert response.status_code == 201
    dish_id = response.json()["id"]

    # delete
    response = client.delete(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    )
    assert response.status_code == 200

    # get submenu by id
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    )
    assert response.status_code == 404

    # get all submenus
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    assert response.status_code == 200
    assert not response.json() or not any(
        map(
            lambda item: item["id"] == dish_id,
            response.json(),
        )
    )

    # check all menus!
    menus = client.get(f"/api/v1/menus/").json()
    for menu in menus:
        submenus = client.get(f"/api/v1/menus/{menu['id']}/submenus").json()
        for submenu in submenus:
            dishes = client.get(
                f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/"
            ).json()
            assert not dishes or not any(
                map(
                    lambda item: item["id"] == dish_id,
                    dishes,
                )
            )


def test_delete_submenu_not_exist(db_create_submenus, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    submenu_id = "00000000-0000-0000-0000-000000000000"
    dish_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    )
    assert response.status_code == 404
