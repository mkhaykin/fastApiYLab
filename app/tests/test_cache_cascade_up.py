"""
    на момент теста у нас 2 записи по меню, 3 записи submenu и 3 записи dish
    00000000-0001-0000-0000-000000000000
        00000000-0000-0001-0000-000000000000
            00000000-0000-0000-0001-000000000000
            00000000-0000-0000-0002-000000000000
        00000000-0000-0002-0000-000000000000
            00000000-0000-0000-0003-000000000000
    00000000-0002-0000-0000-000000000000
        00000000-0000-0003-0000-000000000000

"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.cache.actions import cache_get
from app.tests.utils import random_word


@pytest.mark.asyncio
async def test_dishes_count(db_create_dishes: AsyncSession, async_client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200

    # кладем в кэш меню
    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    # кладем в кэш подменю
    response = await async_client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200

    # создаем блюдо
    response = await async_client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json={
            'title': f'{random_word(10)}',
            'description': f'{random_word(20)}',
            'price': '1',
        },
    )
    assert response.status_code == 201
    dish_id = response.json()['id']

    assert (await cache_get(menu_id, 'menu')) is None
    assert (await cache_get(submenu_id, 'submenu')) is None

    # check count: submenu + 1
    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert (await cache_get(menu_id, 'menu'))

    # delete dish
    response = await async_client.delete(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    assert response.status_code == 200
    assert (await cache_get(menu_id, 'menu')) is None
    assert (await cache_get(submenu_id, 'submenu')) is None

    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200

    assert (await cache_get(menu_id, 'menu'))
