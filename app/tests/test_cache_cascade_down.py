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

from .utils_dish import dish_in_cache
from .utils_menu import menu_in_cache
from .utils_submenu import submenu_in_cache


@pytest.mark.asyncio
async def test_cache_submenu_cascade_drop_after_drop(db_create_dishes: AsyncSession, async_client: AsyncClient):
    # сброс кэша после каскадного удаления
    # кладем в кэш меню
    menu_id = '00000000-0001-0000-0000-000000000000'
    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200

    # кладем в кэш подменю
    submenu_id = '00000000-0000-0001-0000-000000000000'
    response = await async_client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200

    # кладем в кэш блюдо
    dish_id = '00000000-0000-0000-0001-000000000000'
    response = await async_client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200

    # удаляем, кэш должен быть очищен
    response = await async_client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200

    assert not (await menu_in_cache(menu_id))
    assert not (await submenu_in_cache(menu_id, submenu_id))
    assert not (await dish_in_cache(menu_id, submenu_id, dish_id))
