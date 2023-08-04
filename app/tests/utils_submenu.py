from starlette.testclient import TestClient


def get_submenu(client: TestClient, menu_id: str, submenu_id: str) -> dict:
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'description' in response.json()
    assert 'dishes_count' in response.json()
    return response.json()


def create_submenu(
    client: TestClient, menu_id: str, title: str, description: str
) -> str:
    response = client.post(
        f'/api/v1/menus/{menu_id}/submenus',
        json={'title': title, 'description': description},
    )
    assert response.status_code == 201

    submenu_id: str = response.json()['id']
    assert response.json() == {
        'id': submenu_id,
        'menu_id': menu_id,
        'title': title,
        'description': description,
        'dishes_count': 0,
    }
    return submenu_id


def patch_submenu(
    client: TestClient, menu_id: str, submenu_id: str, title: str, description: str
):
    data = get_submenu(client, menu_id, submenu_id)
    dishes_count = data['dishes_count']

    response = client.patch(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
        json={
            'title': title,
            'description': description,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': submenu_id,
        'menu_id': menu_id,
        'title': title,
        'description': description,
        'dishes_count': dishes_count,
    }


def check_submenu_eq_submenu(client: TestClient, submenu: dict):
    data = get_submenu(client, submenu['menu_id'], submenu['id'])
    assert data == submenu


def check_submenu_in_submenus(client: TestClient, submenu: dict):
    response = client.get(f"/api/v1/menus/{submenu['menu_id']}/submenus/")
    assert response.status_code == 200
    assert response.json() and any(
        map(
            lambda item: item == submenu,
            response.json(),
        )
    )


def check_submenu_not_in_submenus(
    client: TestClient, menu_id: str, submenu_id: str
):
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/')
    assert response.status_code == 200
    assert not response.json() or not any(
        map(
            lambda item: item['id'] == submenu_id,
            response.json(),
        )
    )
