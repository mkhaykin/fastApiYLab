from httpx import AsyncClient

from .utils import compare_response


async def get_menu(client: AsyncClient, menu_id: str) -> dict:
    response = await client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'description' in response.json()
    # assert 'submenus_count' in response.json()
    # assert 'dishes_count' in response.json()
    return response.json()


async def create_menu(client: AsyncClient, title: str, description: str) -> str:
    response = await client.post(
        '/api/v1/menus',
        json={
            'title': f'{title}',
            'description': f'{description}',
        },
    )
    assert response.status_code == 201
    menu_id = response.json()['id']

    assert compare_response(answer=response.json(),
                            standard={
        'id': menu_id,
        'title': title,
        'description': description,
        # 'submenus_count': 0,
        # 'dishes_count': 0,
    })
    return menu_id


async def patch_menu(client: AsyncClient, menu_id: str, title: str, description: str):
    # data = await get_menu(client, menu_id)
    # submenus_count = data['submenus_count']
    # dishes_count = data['dishes_count']
    response = await client.patch(
        f'/api/v1/menus/{menu_id}',
        json={
            'title': title,
            'description': description,
        },
    )
    assert response.status_code == 200
    assert compare_response(answer=response.json(),
                            standard={
        'id': menu_id,
        'title': title,
        'description': description,
        # 'submenus_count': submenus_count,
        # 'dishes_count': dishes_count,
    })


async def check_menu_eq_menu(client: AsyncClient, menu: dict):
    data = await get_menu(client, menu['id'])
    assert compare_response(data, menu)


async def check_menu_in_menus(client: AsyncClient, menu: dict):
    response = await client.get('/api/v1/menus')
    assert response.status_code == 200
    assert response.json() and any(
        map(
            lambda item: compare_response(item, menu),
            response.json(),
        )
    )


async def check_menu_not_in_menus(client: AsyncClient, menu_id: str):
    response = await client.get('/api/v1/menus')

    assert response.status_code == 200
    assert not response.json() or not any(
        map(
            lambda item: item['id'] == menu_id,
            response.json(),
        )
    )
