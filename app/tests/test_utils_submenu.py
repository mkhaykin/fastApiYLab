from httpx import AsyncClient

from app.tests.test_utils import compare_response
from app.tests.test_utils_cache import key_pattern_in_cache


async def get_submenus(
        client: AsyncClient,
        menu_id: str,
        waited_code: int = 200,
) -> list[dict]:
    response = await client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert response.status_code == waited_code
    if response.status_code == 200:
        for item in response.json():
            assert 'id' in item
            assert 'title' in item
            assert 'description' in item
            assert 'dishes_count' in item
    return response.json()


async def get_submenu(
        client: AsyncClient,
        menu_id: str,
        submenu_id: str,
        waited_code: int = 200,
) -> dict:
    response = await client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == waited_code
    if response.status_code == 200:
        assert 'id' in response.json()
        assert 'title' in response.json()
        assert 'description' in response.json()
        assert 'dishes_count' in response.json()
    return response.json()


async def create_submenu(
        client: AsyncClient,
        menu_id: str,
        title: str,
        description: str,
        waited_code: int = 201,
):
    response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus',
        json={'title': title, 'description': description},
    )
    assert response.status_code == waited_code
    if response.status_code == 201:
        submenu_id: str = response.json()['id']
        assert compare_response(answer=response.json(),
                                expected_answer={
                                    'id': submenu_id,
                                    'menu_id': menu_id,
                                    'title': title,
                                    'description': description,
        })
        return submenu_id
    return response.json()


async def patch_submenu(
        client: AsyncClient,
        menu_id: str,
        submenu_id: str,
        title: str,
        description: str,
        waited_code: int = 200,
):
    response = await client.patch(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
        json={
            'title': title,
            'description': description,
        },
    )
    assert response.status_code == waited_code
    if response.status_code == 200:
        assert compare_response(answer=response.json(),
                                expected_answer={
                                    'id': submenu_id,
                                    'menu_id': menu_id,
                                    'title': title,
                                    'description': description,
        })
    return response.json()


async def delete_submenu(
        client: AsyncClient,
        menu_id: str,
        submenu_id: str,
        waited_code: int = 200,
):
    response = await client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == waited_code
    return response.json()


async def check_submenu_eq_submenu(
        client: AsyncClient,
        submenu: dict
):
    data = await get_submenu(client, submenu['menu_id'], submenu['id'])
    assert compare_response(data, submenu)


async def check_submenu_in_submenus(
        client: AsyncClient,
        submenu: dict,
):
    response = await client.get(f"/api/v1/menus/{submenu['menu_id']}/submenus")
    assert response.status_code == 200
    assert response.json() and any(
        map(
            lambda item: compare_response(item, submenu),
            response.json(),
        )
    )


async def check_submenu_not_in_submenus(
        client: AsyncClient,
        menu_id: str,
        submenu_id: str,
):
    response = await client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert response.status_code == 200
    assert not response.json() or not any(
        map(
            lambda item: item['id'] == submenu_id,
            response.json(),
        )
    )


async def check_submenu_not_exists(
        client: AsyncClient,
        submenu_id: str,
):
    """
    Проверяет, что подменю не встретится ни в каких меню
    :param client:
    :param submenu_id:
    :return:
    """
    # check all menus!
    menus = (await client.get('/api/v1/menus')).json()
    for menu in menus:
        await check_submenu_not_in_submenus(client, menu['id'], submenu_id)


async def submenu_in_cache(
        menu_id: str,
        submenu_id: str,
):
    return await key_pattern_in_cache(f'*:{menu_id}:{submenu_id}:None')


async def submenus_in_cache(
        menu_id: str,
):
    return await key_pattern_in_cache(f'*:{menu_id}:None:None')
