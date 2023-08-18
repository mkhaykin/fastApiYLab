import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.test_utils import random_word
from app.tests.test_utils_menu import menu_in_cache
from app.tests.test_utils_submenu import submenu_in_cache


@pytest.mark.asyncio
async def test_dishes_count(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200

    # Кладем в кэш меню
    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    # кладем в кэш подменю
    response = await async_client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200

    # Создаем блюдо
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

    # Кэша нет, т.к. создание блюда должно сбросить кеш и меню и подменю
    assert not (await menu_in_cache(menu_id))
    assert not (await submenu_in_cache(menu_id, submenu_id))

    # Кладем в кеш меню
    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    # Проверяем что есть
    assert (await menu_in_cache(menu_id))

    # Удаляем блюдо
    response = await async_client.delete(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    assert response.status_code == 200

    # Меню не в кэше
    assert not (await menu_in_cache(menu_id))
    # Подменю не в кэше
    assert not (await submenu_in_cache(menu_id, submenu_id))

    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200

    assert (await menu_in_cache(menu_id))
