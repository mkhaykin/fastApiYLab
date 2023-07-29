from uuid import UUID

from app.tests.utils import random_word


def test_alive(db_test, client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_menu(db_test, client):
    # step 1, empty result
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    # assert not response.json()    # data must be cleared for this test

    # step 2, 404 error
    response = client.get("/api/v1/menus/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}

    # step 3, create menu
    menu_for_create = {
        "title": f"{random_word(10)}",
        "description": f"{random_word(20)}",
    }
    response = client.post("/api/v1/menus", json=menu_for_create)
    assert response.status_code == 201
    assert "id" in response.json()

    menu_id: UUID = response.json()["id"]
    menu_created = {"id": menu_id, "submenus_count": 0, "dishes_count": 0}
    menu_created.update(menu_for_create)

    assert "title" in response.json()
    assert "description" in response.json()
    assert response.json()["title"] == menu_created["title"]
    assert response.json()["description"] == menu_created["description"]

    # step 4, get all menus
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert menu_created in response.json()

    # step 5, get menus with id equal menu_id
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json() == menu_created

    # step 6, update menu
    menu_update = {"title": f"{random_word(10)}", "description": f"{random_word(20)}"}
    response = client.patch(f"/api/v1/menus/{menu_id}", json=menu_update)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert response.json()["id"] == menu_id
    assert response.json()["title"] == menu_update["title"]
    assert response.json()["description"] == menu_update["description"]

    # step 7, check updated menu
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert response.json()["id"] == menu_id
    assert response.json()["title"] == menu_update["title"]
    assert response.json()["description"] == menu_update["description"]

    # step 8, delete menu
    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200

    # step 9, get menus with id equal menu_id
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}


def test_submenu(db_test, client):
    # step 1, empty result
    response = client.get("/api/v1/menus")
    assert response.status_code == 200

    # step 2, create menu
    menu_for_create = {
        "title": f"{random_word(10)}",
        "description": f"{random_word(20)}",
    }
    response = client.post("/api/v1/menus", json=menu_for_create)
    assert response.status_code == 201
    assert "id" in response.json()

    menu_id: UUID = response.json()["id"]
    menu_created = {"id": menu_id, "submenus_count": 0, "dishes_count": 0}
    menu_created.update(menu_for_create)

    assert "title" in response.json()
    assert "description" in response.json()
    # assert response.json()["title"] == menu_created["title"]
    # assert response.json()["description"] == menu_created["description"]
    assert response.json() == menu_created

    # step 3, get all menus
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert menu_created in response.json()

    # step 4, get menus with id equal menu_id
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json() == menu_created

    # step 4.1 empty answer
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert not response.json()

    # step 4.2 check specific submenu
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}

    # step 4.1 check wrong menu
    response = client.get(
        f"/api/v1/menus/00000000-0000-0000-0000-000000000000/submenus/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}

    # step 5, create sub menu 1
    submenu_for_create = {
        "title": f"{random_word(10)}",
        "description": f"{random_word(20)}",
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu_for_create)
    assert response.status_code == 201
    assert "id" in response.json()

    submenu1_id: UUID = response.json()["id"]
    submenu1_created = {"id": submenu1_id, "dishes_count": 0}
    submenu1_created.update({"menu_id": menu_id})
    submenu1_created.update(submenu_for_create)
    menu_created["submenus_count"] += 1

    assert "title" in response.json()
    assert "description" in response.json()
    assert response.json()["title"] == submenu1_created["title"]
    assert response.json()["description"] == submenu1_created["description"]

    # step 6, get all submenu
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert response.json() == [submenu1_created]

    # step 7, get specific submenu
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu1_id}")
    assert response.status_code == 200
    assert response.json() == submenu1_created

    # step 8, create sub menu 2
    submenu_for_create = {
        "title": f"{random_word(10)}",
        "description": f"{random_word(20)}",
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu_for_create)
    assert response.status_code == 201
    assert "id" in response.json()

    submenu2_id: UUID = response.json()["id"]
    submenu2_created = {"id": submenu2_id, "dishes_count": 0}
    submenu2_created.update({"menu_id": menu_id})
    submenu2_created.update(submenu_for_create)
    menu_created["submenus_count"] += 1

    assert "title" in response.json()
    assert "description" in response.json()
    assert response.json()["title"] == submenu2_created["title"]
    assert response.json()["description"] == submenu2_created["description"]

    # step 8.1, create sub menu like 2
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu_for_create)
    assert response.status_code == 409
    assert response.json() == {"detail": "the submenu is duplicated"}

    # step 9, get all submenu
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert submenu1_created in response.json()
    assert submenu2_created in response.json()

    # step 9.1, PATCH submenu2
    submenu_update = {
        "title": f"{random_word(10)}",
        "description": f"{random_word(20)}",
    }
    response = client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu2_id}", json=submenu_update
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    submenu2_created["title"] = submenu_update["title"]
    submenu2_created["description"] = submenu_update["description"]

    # step 10, get specific submenu
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu2_id}")
    assert response.status_code == 200
    assert response.json() == submenu2_created

    # step 11, delete submenu2
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu2_id}")
    assert response.status_code == 200
    menu_created["submenus_count"] -= 1

    # step 12, get all submenu
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert submenu1_created in response.json()
    assert submenu2_created not in response.json()

    # step 13, get specific submenu
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu2_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}

    # step 14, delete menu
    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200

    # step 15, if menu is not exist return empty list
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert response.json() == []


def test_dishes(db_test, client):
    # step 1, empty result
    response = client.get("/api/v1/menus")
    assert response.status_code == 200

    # step 2, create menu
    menu_for_create = {
        "title": f"{random_word(10)}",
        "description": f"{random_word(20)}",
    }
    response = client.post("/api/v1/menus", json=menu_for_create)
    assert response.status_code == 201
    assert "id" in response.json()

    menu_id: UUID = response.json()["id"]
    menu_created = {"id": menu_id, "submenus_count": 0, "dishes_count": 0}
    menu_created.update(menu_for_create)

    assert "title" in response.json()
    assert "description" in response.json()
    assert response.json()["title"] == menu_created["title"]
    assert response.json()["description"] == menu_created["description"]

    # step 4, get menus with id equal menu_id
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json() == menu_created

    # step 4.1 empty answer
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert not response.json()

    # step 5, create sub menu 1
    submenu_for_create = {
        "title": f"{random_word(10)}",
        "description": f"{random_word(20)}",
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu_for_create)
    assert response.status_code == 201
    assert "id" in response.json()

    submenu1_id: UUID = response.json()["id"]
    submenu1_created = {"id": submenu1_id, "dishes_count": 0}
    submenu1_created.update({"menu_id": menu_id})
    submenu1_created.update(submenu_for_create)

    menu_created["submenus_count"] += 1

    assert "title" in response.json()
    assert "description" in response.json()
    assert response.json()["title"] == submenu1_created["title"]
    assert response.json()["description"] == submenu1_created["description"]

    # step 6, get all submenu
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert response.json() == [submenu1_created]

    # step 7, get specific submenu
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu1_id}")
    assert response.status_code == 200
    assert response.json() == submenu1_created

    # step 8, create sub menu 2
    submenu_for_create = {
        "title": f"{random_word(10)}",
        "description": f"{random_word(20)}",
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu_for_create)
    assert response.status_code == 201
    assert "id" in response.json()

    submenu2_id: UUID = response.json()["id"]
    submenu2_created = {"id": submenu2_id, "dishes_count": 0}
    submenu2_created.update({"menu_id": menu_id})
    submenu2_created.update(submenu_for_create)

    menu_created["submenus_count"] += 1

    assert "title" in response.json()
    assert "description" in response.json()
    assert response.json()["title"] == submenu2_created["title"]
    assert response.json()["description"] == submenu2_created["description"]

    # step 9, get all submenu
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert submenu1_created in response.json()
    assert submenu2_created in response.json()

    # step 9.1, empty dishes list
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu1_id}/dishes")
    assert response.status_code == 200
    assert not response.json()
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu2_id}/dishes")
    assert response.status_code == 200
    assert not response.json()

    # step 10, create dishes 1
    dish_for_create = {
        "title": f"{random_word(10)}",
        "description": f"{random_word(20)}",
        "price": "10.5",
    }
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu1_id}/dishes", json=dish_for_create
    )
    assert response.status_code == 201
    assert "id" in response.json()

    dish11_id: UUID = response.json()["id"]
    dish11_created = {"id": dish11_id}
    dish11_created.update({"submenu_id": submenu1_id})
    dish11_created.update(dish_for_create)

    submenu1_created["dishes_count"] += 1

    assert "title" in response.json()
    assert "description" in response.json()
    assert response.json()["title"] == dish11_created["title"]
    assert response.json()["description"] == dish11_created["description"]
    assert response.json()["price"] == dish11_created["price"]

    # step 11, create dishes 2
    dish_for_create = {
        "title": f"{random_word(10)}",
        "description": f"{random_word(20)}",
        "price": "10",
    }
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu1_id}/dishes", json=dish_for_create
    )
    assert response.status_code == 201
    assert "id" in response.json()

    dish12_id: UUID = response.json()["id"]
    dish12_created = {"id": dish12_id}
    dish12_created.update({"submenu_id": submenu1_id})
    dish12_created.update(dish_for_create)

    submenu1_created["dishes_count"] += 1

    assert "title" in response.json()
    assert "description" in response.json()
    assert response.json()["title"] == dish12_created["title"]
    assert response.json()["description"] == dish12_created["description"]
    assert response.json()["price"] == "10.0"  # dish12_created["price"]

    # step 12, create dishes 3
    dish_for_create = {
        "title": f"{random_word(10)}",
        "description": f"{random_word(20)}",
        "price": "10.567",
    }
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu2_id}/dishes", json=dish_for_create
    )
    assert response.status_code == 201
    assert "id" in response.json()

    dish21_id: UUID = response.json()["id"]
    dish21_created = {"id": dish21_id}
    dish21_created.update({"submenu_id": submenu2_id})
    dish21_created.update(dish_for_create)

    submenu2_created["dishes_count"] += 1

    assert "title" in response.json()
    assert "description" in response.json()
    assert response.json()["title"] == dish21_created["title"]
    assert response.json()["description"] == dish21_created["description"]
    assert response.json()["price"] == "10.57"  # dish21_created["price"]

    # PATH dish11
    # step 13, PATCH submenu1
    dish_update = {
        "title": f"{random_word(10)}",
        "description": f"{random_word(20)}",
        "price": "0.01",
    }
    response = client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu1_id}/dishes/{dish11_id}",
        json=dish_update,
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert "price" in response.json()
    dish11_created["title"] = dish_update["title"]
    dish11_created["description"] = dish_update["description"]
    dish11_created["price"] = dish_update["price"]

    # step 14, GET dish11
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu1_id}/dishes/{dish11_id}"
    )
    assert response.status_code == 200
    assert response.json() == dish11_created

    # step 15, GET dish11 from submenu2: 404
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu2_id}/dishes/{dish11_id}"
    )
    assert response.status_code == 404

    # DELETE dish11

    # GET dish11 not in res, buh dish12 in.

    # DELETE submenu 1

    # GET check dish21 in submenu2

    # GET check submenu1: 404

    # # step 16, delete menu
    # response = client.delete(f"/api/v1/menus/{menu_id}")
    # assert response.status_code == 200
    #
    # # step 17, if menu is not exist return empty list
    # response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    # assert response.status_code == 200
    # assert response.json() == []
