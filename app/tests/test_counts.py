import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.test_utils import random_word
from app.tests.test_utils_dish import create_dish, delete_dish
from app.tests.test_utils_menu import get_menu
from app.tests.test_utils_submenu import create_submenu, delete_submenu


@pytest.mark.asyncio
async def test_submenus_count(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'

    # get start values
    data = await get_menu(async_client, menu_id)
    submenus_count = data['submenus_count']
    dishes_count = data['dishes_count']

    # create submenu
    submenu_id = await create_submenu(async_client, menu_id, random_word(10), random_word(20))

    # check count: submenu + 1
    data = await get_menu(async_client, menu_id)
    assert data['submenus_count'] == submenus_count + 1
    assert data['dishes_count'] == dishes_count

    # delete submenu
    await delete_submenu(async_client, menu_id, submenu_id)

    # check count: submenu back to start value
    data = await get_menu(async_client, menu_id)
    assert data['submenus_count'] == submenus_count
    assert data['dishes_count'] == dishes_count


@pytest.mark.asyncio
async def test_dishes_count(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'

    # get start values
    data = await get_menu(async_client, menu_id)
    submenus_count = data['submenus_count']
    dishes_count = data['dishes_count']

    # create dish
    dish_id = await create_dish(async_client, menu_id, submenu_id, random_word(10), random_word(20), '1.11')

    # check count: submenu + 1
    data = await get_menu(async_client, menu_id)
    assert data['submenus_count'] == submenus_count
    assert data['dishes_count'] == dishes_count + 1

    # delete dish
    await delete_dish(async_client, menu_id, submenu_id, dish_id)

    # check count: submenu start value
    data = await get_menu(async_client, menu_id)
    assert data['submenus_count'] == submenus_count
    assert data['dishes_count'] == dishes_count
