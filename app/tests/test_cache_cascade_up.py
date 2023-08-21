import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.test_data import DISH_ID111, MENU_ID1, SUBMENU_ID11
from app.tests.test_utils import random_word
from app.tests.test_utils_dish import create_dish, delete_dish, dish_in_cache, get_dish
from app.tests.test_utils_menu import get_menu, menu_in_cache
from app.tests.test_utils_submenu import get_submenu, submenu_in_cache


@pytest.mark.asyncio
async def test_cache_dishes_create(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11
    dish_id = DISH_ID111
    # Кладем в кэш меню
    await get_menu(async_client, menu_id)
    # кладем в кэш подменю
    await get_submenu(async_client, menu_id, submenu_id)
    # кладем в кэш блюдо
    await get_dish(async_client, menu_id, submenu_id, dish_id)

    # Создаем блюдо
    created_dish_id = await create_dish(async_client, menu_id, submenu_id, random_word(10), random_word(20), '1.11')

    # Кэша нет у меню, подменю, нового блюда и "старого" блюда
    assert not (await menu_in_cache(menu_id))
    assert not (await submenu_in_cache(menu_id, submenu_id))
    assert not (await dish_in_cache(menu_id, submenu_id, dish_id))
    assert not (await dish_in_cache(menu_id, submenu_id, created_dish_id))


@pytest.mark.asyncio
async def test_cache_dishes_delete(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11
    dish_id = DISH_ID111
    # Кладем в кэш меню
    await get_menu(async_client, menu_id)
    # кладем в кэш подменю
    await get_submenu(async_client, menu_id, submenu_id)
    # кладем в кэш блюдо
    await get_dish(async_client, menu_id, submenu_id, dish_id)

    # удаляем блюдо
    await delete_dish(async_client, menu_id, submenu_id, dish_id)

    # Кэша нет у меню, подменю и нового блюда. Есть у "старого" блюда
    assert not (await menu_in_cache(menu_id))
    assert not (await submenu_in_cache(menu_id, submenu_id))
    assert not (await dish_in_cache(menu_id, submenu_id, dish_id))
