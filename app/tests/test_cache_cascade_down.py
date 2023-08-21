import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.test_data import DISH_ID111, MENU_ID1, SUBMENU_ID11
from app.tests.test_utils_dish import dish_in_cache, get_dish
from app.tests.test_utils_menu import delete_menu, get_menu, menu_in_cache
from app.tests.test_utils_submenu import get_submenu, submenu_in_cache


@pytest.mark.asyncio
async def test_cache_submenu_cascade_drop_after_drop(db_test_data: AsyncSession, async_client: AsyncClient):
    # сброс кэша после каскадного удаления
    # кладем в кэш меню
    menu_id = MENU_ID1
    await get_menu(async_client, menu_id)

    # кладем в кэш подменю
    submenu_id = SUBMENU_ID11
    await get_submenu(async_client, menu_id, submenu_id)

    # кладем в кэш блюдо
    dish_id = DISH_ID111
    await get_dish(async_client, menu_id, submenu_id, dish_id)

    # удаляем, кэш должен быть очищен
    await delete_menu(async_client, menu_id)

    assert not (await menu_in_cache(menu_id))
    assert not (await submenu_in_cache(menu_id, submenu_id))
    assert not (await dish_in_cache(menu_id, submenu_id, dish_id))
