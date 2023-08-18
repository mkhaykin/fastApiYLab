from httpx import AsyncClient

from app.tests.test_utils import compare_response
from app.tests.test_utils_cache import key_pattern_in_cache


async def get_menus(
        client: AsyncClient,
        waited_code: int = 200,
) -> list[dict]:
    response = await client.get('/api/v1/menus')
    assert response.status_code == waited_code
    if waited_code == 200:
        for item in response.json():
            assert 'id' in item
            assert 'title' in item
            assert 'description' in item
            assert 'submenus_count' in item
            assert 'dishes_count' in item
    return response.json()


async def get_menu(
        client: AsyncClient,
        menu_id: str,
        waited_code: int = 200,
) -> dict:
    response = await client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == waited_code
    if waited_code == 200:
        assert 'id' in response.json()
        assert 'title' in response.json()
        assert 'description' in response.json()
        assert 'submenus_count' in response.json()
        assert 'dishes_count' in response.json()
    return response.json()


async def create_menu(
        client: AsyncClient,
        title: str,
        description: str,
        waited_code: int = 201,
):
    response = await client.post(
        '/api/v1/menus',
        json={
            'title': f'{title}',
            'description': f'{description}',
        },
    )
    assert response.status_code == waited_code
    if response.status_code == 201:
        menu_id = response.json()['id']

        assert compare_response(answer=response.json(),
                                expected_answer={
                                    'id': menu_id,
                                    'title': title,
                                    'description': description,
        })
        return menu_id
    return response.json()


async def patch_menu(
        client: AsyncClient,
        menu_id: str,
        title: str,
        description: str,
        waited_code: int = 200,
):
    response = await client.patch(
        f'/api/v1/menus/{menu_id}',
        json={
            'title': title,
            'description': description,
        },
    )
    assert response.status_code == waited_code

    if response.status_code == 200:
        assert compare_response(
            answer=response.json(),
            expected_answer={
                'id': menu_id,
                'title': title,
                'description': description,
            })
    return response.json()


async def delete_menu(
        client: AsyncClient,
        menu_id: str,
        waited_code: int = 200,
):
    response = await client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == waited_code
    return response.json()


async def check_menu_eq_menu(
        client: AsyncClient,
        menu: dict,
):
    data = await get_menu(client, menu['id'])
    assert compare_response(data, menu)


async def check_menu_in_menus(
        client: AsyncClient,
        menu: dict,
):
    response = await client.get('/api/v1/menus')
    assert response.status_code == 200
    assert response.json() and any(
        map(
            lambda item: compare_response(item, menu),
            response.json(),
        )
    )


async def check_menu_not_in_menus(
        client: AsyncClient,
        menu_id: str,
):
    response = await client.get('/api/v1/menus')

    assert response.status_code == 200
    assert not response.json() or not any(
        map(
            lambda item: item['id'] == menu_id,
            response.json(),
        )
    )


async def menu_in_cache(
        menu_id: str
):
    return await key_pattern_in_cache(f'*:{menu_id}:None:None')


async def menus_in_cache():
    return await key_pattern_in_cache('*:None:None:None')
