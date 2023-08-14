from httpx import AsyncClient

from .utils import compare_response


async def get_submenu(client: AsyncClient, menu_id: str, submenu_id: str) -> dict:
    response = await client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'description' in response.json()
    # assert 'dishes_count' in response.json()
    return response.json()


async def create_submenu(
        client: AsyncClient, menu_id: str, title: str, description: str
) -> str:
    response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus',
        json={'title': title, 'description': description},
    )
    assert response.status_code == 201

    submenu_id: str = response.json()['id']
    assert compare_response(answer=response.json(),
                            standard={
                                'id': submenu_id,
                                'menu_id': menu_id,
                                'title': title,
                                'description': description,
                                # 'dishes_count': 0,
    })
    return submenu_id


async def patch_submenu(
        client: AsyncClient, menu_id: str, submenu_id: str, title: str, description: str
):
    # data = await get_submenu(client, menu_id, submenu_id)
    # dishes_count = data['dishes_count']
    response = await client.patch(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
        json={
            'title': title,
            'description': description,
        },
    )
    assert response.status_code == 200
    assert compare_response(answer=response.json(),
                            standard={
                                'id': submenu_id,
                                'menu_id': menu_id,
                                'title': title,
                                'description': description,
                                # 'dishes_count': dishes_count,
    })


async def check_submenu_eq_submenu(client: AsyncClient, submenu: dict):
    data = await get_submenu(client, submenu['menu_id'], submenu['id'])
    assert compare_response(data, submenu)


async def check_submenu_in_submenus(client: AsyncClient, submenu: dict):
    response = await client.get(f"/api/v1/menus/{submenu['menu_id']}/submenus")
    assert response.status_code == 200
    assert response.json() and any(
        map(
            lambda item: compare_response(item, submenu),
            response.json(),
        )
    )


async def check_submenu_not_in_submenus(
        client: AsyncClient, menu_id: str, submenu_id: str
):
    response = await client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert response.status_code == 200
    assert not response.json() or not any(
        map(
            lambda item: item['id'] == submenu_id,
            response.json(),
        )
    )
