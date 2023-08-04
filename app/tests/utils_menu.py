from uuid import UUID

from app.tests.database import TestingSession


def get_menu(client: TestingSession, menu_id: UUID) -> dict:
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert "submenus_count" in response.json()
    assert "dishes_count" in response.json()
    return response.json()


def create_menu(client: TestingSession, title: str, description: str) -> UUID:
    response = client.post(
        "/api/v1/menus",
        json={
            "title": f"{title}",
            "description": f"{description}",
        },
    )
    assert response.status_code == 201
    menu_id = response.json()["id"]

    assert response.json() == {
        "id": menu_id,
        "title": title,
        "description": description,
        "submenus_count": 0,
        "dishes_count": 0,
    }
    return menu_id


def patch_menu(client: TestingSession, menu_id: UUID, title: str, description: str):
    data = get_menu(client, menu_id)
    submenus_count = data["submenus_count"]
    dishes_count = data["dishes_count"]

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
        "submenus_count": submenus_count,
        "dishes_count": dishes_count,
    }


def check_menu_eq_menu(client: TestingSession, menu: dict):
    data = get_menu(client, menu["id"])
    assert data == menu


def check_menu_in_menus(client: TestingSession, menu: dict):
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() and any(
        map(
            lambda item: item == menu,
            response.json(),
        )
    )


def check_menu_not_in_menus(client: TestingSession, menu_id: UUID):
    response = client.get(f"/api/v1/menus/")
    assert response.status_code == 200
    assert not response.json() or not any(
        map(
            lambda item: item["id"] == menu_id,
            response.json(),
        )
    )
