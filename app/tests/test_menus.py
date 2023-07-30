from app.tests.utils import random_word


def test_menus(db_test, client):
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    # assert not response.json()    # data must be cleared for this test


def test_menu_not_found(db_test, client):
    response = client.get("/api/v1/menus/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}


def test_create_menu_fix(db_test, client):
    response = client.post(
        "/api/v1/menus",
        json={"title": "My menu 1", "description": "My menu description 1"},
    )
    assert response.status_code == 201
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()

    menu_id = response.json()["id"]
    assert response.json() == {
        "id": menu_id,
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0,
    }


def test_create_menu_duplicate(db_test, client):
    response = client.post(
        "/api/v1/menus",
        json={"title": "My menu 1", "description": "My menu description 1"},
    )
    assert response.status_code == 409


def test_create_menu(db_test, client):
    title = random_word(10)
    description = random_word(20)
    response = client.post(
        "/api/v1/menus",
        json={
            "title": f"{title}",
            "description": f"{description}",
        },
    )
    assert response.status_code == 201
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()

    menu_id = response.json()["id"]
    assert response.json() == {
        "id": menu_id,
        "title": title,
        "description": description,
        "submenus_count": 0,
        "dishes_count": 0,
    }


def test_create_menu_and_find_it(db_test, client):
    # create
    title = random_word(11)
    description = random_word(20)
    response = client.post(
        "/api/v1/menus",
        json={
            "title": f"{title}",
            "description": f"{description}",
        },
    )
    assert response.status_code == 201
    menu_id = response.json()["id"]
    # get menu by id
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": menu_id,
        "title": title,
        "description": description,
        "submenus_count": 0,
        "dishes_count": 0,
    }


def test_create_menu_and_find_it_in_menus(db_test, client):
    # create
    title = random_word(12)
    description = random_word(20)
    response = client.post(
        "/api/v1/menus",
        json={
            "title": f"{title}",
            "description": f"{description}",
        },
    )
    assert response.status_code == 201
    menu_id = response.json()["id"]
    # get all menus
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() and any(
        map(
            lambda item: item
            == {
                "id": menu_id,
                "title": title,
                "description": description,
                "submenus_count": 0,
                "dishes_count": 0,
            },
            response.json(),
        )
    )


def test_update_menu_and_find_it(db_test, client):
    response = client.post(
        "/api/v1/menus",
        json={
            "title": f"{random_word(13)}",
            "description": f"{random_word(20)}",
        },
    )
    assert response.status_code == 201

    menu_id = response.json()["id"]
    # new value
    title = random_word(14)
    description = random_word(20)

    # patch
    response = client.patch(
        f"/api/v1/menus/{menu_id}",
        json={
            "title": title,
            "description": description,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": menu_id,
        "title": title,
        "description": description,
        "submenus_count": 0,
        "dishes_count": 0,
    }

    # check get
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": menu_id,
        "title": title,
        "description": description,
        "submenus_count": 0,
        "dishes_count": 0,
    }


def test_update_menu_and_find_it_in_menus(db_test, client):
    response = client.post(
        "/api/v1/menus",
        json={
            "title": f"{random_word(15)}",
            "description": f"{random_word(20)}",
        },
    )
    assert response.status_code == 201

    menu_id = response.json()["id"]
    # new value
    title = random_word(16)
    description = random_word(20)

    # patch
    response = client.patch(
        f"/api/v1/menus/{menu_id}",
        json={
            "title": title,
            "description": description,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": menu_id,
        "title": title,
        "description": description,
        "submenus_count": 0,
        "dishes_count": 0,
    }

    # check get
    response = client.get(f"/api/v1/menus/")
    assert response.status_code == 200  #
    assert response.json() and any(
        map(
            lambda item: item
            == {
                "id": menu_id,
                "title": title,
                "description": description,
                "submenus_count": 0,
                "dishes_count": 0,
            },
            response.json(),
        )
    )


def test_delete_menu(db_test, client):
    response = client.post(
        "/api/v1/menus",
        json={
            "title": f"{random_word(17)}",
            "description": f"{random_word(20)}",
        },
    )
    assert response.status_code == 201
    menu_id = response.json()["id"]

    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200


def test_delete_menu_not_exist(db_test, client):
    menu_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 404


def test_delete_menu_and_check(db_test, client):
    # create
    response = client.post(
        "/api/v1/menus",
        json={
            "title": f"{random_word(18)}",
            "description": f"{random_word(20)}",
        },
    )
    assert response.status_code == 201
    menu_id = response.json()["id"]
    # delete
    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    # check by menu_id
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}
    # check in menus
    response = client.get(f"/api/v1/menus/")
    assert response.status_code == 200
    assert not response.json() or not any(
        map(
            lambda item: item["id"] == menu_id,
            response.json(),
        )
    )
