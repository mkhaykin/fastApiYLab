from httpx import AsyncClient

from app.main import app
from app.src.routes import dishes
from app.tests.test_utils import compare_response, round_price
from app.tests.test_utils_cache import key_pattern_in_cache
from app.tests.test_utils_menu import get_menus
from app.tests.test_utils_submenu import get_submenus


def _check_field(data, submenu_id=None, dish_id=None):
    # наличие полей
    assert 'id' in data
    assert 'submenu_id' in data
    assert 'title' in data
    assert 'description' in data
    assert 'price' in data
    # контроль привязок
    assert not submenu_id or data['submenu_id'] == submenu_id
    assert not dish_id or data['id'] == dish_id


async def get_dishes(
        client: AsyncClient,
        menu_id: str,
        submenu_id: str,
        waited_code: int = 200,
) -> list[dict]:
    # response = await client.get(
    #     f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes'
    # )
    response = await client.get(
        app.url_path_for(
            dishes.get_dishes.__name__,
            menu_id=menu_id,
            submenu_id=submenu_id,
        ),
    )
    assert response.status_code == waited_code

    if response.status_code == 200:
        for item in response.json():
            _check_field(item, submenu_id)

    return response.json()


async def get_dish(
        client: AsyncClient,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        waited_code: int = 200,
) -> dict:
    # response = await client.get(
    #     f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    # )
    response = await client.get(
        app.url_path_for(
            dishes.get_dish.__name__,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        ),
    )
    assert response.status_code == waited_code

    if response.status_code == 200:
        _check_field(response.json(), submenu_id, dish_id)

    return response.json()


async def create_dish(
        client: AsyncClient,
        menu_id: str,
        submenu_id: str,
        title: str,
        description: str,
        price: str,
        waited_code: int = 201,
):
    # response = await client.post(
    #     f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    #     json={'title': title, 'description': description, 'price': round_price(price)},
    # )
    response = await client.post(
        app.url_path_for(
            dishes.create_dish.__name__,
            menu_id=menu_id,
            submenu_id=submenu_id,
        ),
        json={
            'title': title,
            'description': description,
            'price': round_price(price)
        },
    )

    assert response.status_code == waited_code

    if response.status_code == 201:
        dishes_id = response.json()['id']
        assert compare_response(answer=response.json(),
                                expected_answer={
                                    'id': dishes_id,
                                    'submenu_id': submenu_id,
                                    'title': title,
                                    'description': description,
                                    'price': round_price(price),
        })
        return dishes_id

    return response.json()


async def patch_dish(
        client: AsyncClient,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        title: str,
        description: str,
        price: str,
        waited_code: int = 200,
):
    # response = await client.patch(
    #     f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    #     json={
    #         'title': title,
    #         'description': description,
    #         'price': price,
    #     },
    # )
    response = await client.patch(
        app.url_path_for(
            dishes.patch_dish.__name__,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        ),
        json={
            'title': title,
            'description': description,
            'price': price,
        },
    )
    assert response.status_code == waited_code
    if response.status_code == 200:
        assert compare_response(answer=response.json(),
                                expected_answer={
                                    'id': dish_id,
                                    'submenu_id': submenu_id,
                                    'title': title,
                                    'description': description,
                                    'price': round_price(price)
        })
    return response.json()


async def delete_dish(
        client: AsyncClient,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        waited_code: int = 200,
):
    # delete
    # response = await client.delete(
    #     f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    # )
    response = await client.delete(
        app.url_path_for(
            dishes.delete_dish.__name__,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        ),
    )
    assert response.status_code == waited_code
    return response.json()


async def check_dish_eq_dish(
        client: AsyncClient,
        menu_id: str,
        dish: dict,
):
    """
    Проверяет, что блюдо присутствует в ответе при запросе из меню и подменю
    :param client:
    :param menu_id:
    :param dish:
    :return:
    """
    data = await get_dish(client, menu_id, dish['submenu_id'], dish['id'])
    assert compare_response(answer=data, expected_answer=dish)


async def check_dish_in_dishes(
        client: AsyncClient,
        menu_id: str,
        dish: dict,
):
    """
    Проверяет, что блюдо присутствует в ответе для блюд подменю конкретного меню
    :param client:
    :param menu_id:
    :param dish:
    :return:
    """
    data = await get_dishes(client, menu_id, dish['submenu_id'])
    assert data and any(
        map(
            lambda item: compare_response(item, dish),
            data,
        )
    )


async def check_dish_not_in_dishes(
        client: AsyncClient,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
):
    """
    Проверяет, что блюдо отсутствует в ответе для блюд подменю конкретного меню
    :param client:
    :param menu_id:
    :param submenu_id:
    :param dish_id:
    :return:
    """
    data = await get_dishes(client, menu_id, submenu_id)
    assert not data or not any(
        map(
            lambda item: item['id'] == dish_id,
            data,
        )
    )


async def check_dish_not_exists(
        client: AsyncClient,
        dish_id: str,
):
    """
    Проверяет, что блюдо не встретится ни в каких подменю никаких меню
    :param client:
    :param dish_id:
    :return:
    """
    # check all menus!
    # menus = (await client.get('/api/v1/menus')).json()
    menus = await get_menus(client)
    for menu in menus:
        # submenus = (await client.get(f"/api/v1/menus/{menu['id']}/submenus")).json()
        submenus = await get_submenus(client, menu['id'])
        for submenu in submenus:
            await check_dish_not_in_dishes(client, menu['id'], submenu['id'], dish_id)


async def dish_in_cache(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
):
    return await key_pattern_in_cache(f'*:{menu_id}:{submenu_id}:{dish_id}')


async def dishes_in_cache(
        menu_id: str,
        submenu_id: str,
):
    return await key_pattern_in_cache(f'*:{menu_id}:{submenu_id}:None')
