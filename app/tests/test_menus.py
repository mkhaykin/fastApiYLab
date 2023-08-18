import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.test_data import MENU1, MENU2, MENU_ID_WRONG
from app.tests.test_utils import compare_response, dict_in_list, random_word
from app.tests.test_utils_menu import (
    check_menu_eq_menu,
    check_menu_in_menus,
    check_menu_not_in_menus,
    create_menu,
    delete_menu,
    get_menu,
    get_menus,
    patch_menu,
)


@pytest.mark.asyncio
async def test_menus(db_test_data: AsyncSession, async_client: AsyncClient):
    data = await get_menus(async_client)
    assert len(data) == 2
    assert dict_in_list(MENU1, data)
    assert dict_in_list(MENU2, data)


@pytest.mark.asyncio
async def test_menu(db_test_data: AsyncSession, async_client: AsyncClient):
    menu = MENU1
    data = await get_menu(async_client, menu['id'])
    compare_response(data, menu)


@pytest.mark.asyncio
async def test_menu_not_found(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID_WRONG
    data = await get_menu(async_client, menu_id, waited_code=404)
    assert data == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_create_menu_fix(db_test_data: AsyncSession, async_client: AsyncClient):
    await create_menu(async_client, 'Menu fixed', 'Menu fixed description 1')


@pytest.mark.asyncio
async def test_create_menu_duplicate(db_test_data: AsyncSession, async_client: AsyncClient):
    title, description = 'My menu 2', 'My menu description 2'
    await create_menu(async_client, title, description)
    await create_menu(async_client, title, description, waited_code=409)


@pytest.mark.asyncio
async def test_create_menu_and_check(db_test_data: AsyncSession, async_client: AsyncClient):
    # create
    title: str = random_word(11)
    description: str = random_word(20)
    menu_id: str = await create_menu(async_client, title, description)

    # check
    answer = {
        'id': menu_id,
        'title': title,
        'description': description,
        'submenus_count': 0,
        'dishes_count': 0,
    }

    # созданное меню должно вернуться при запросе меню по id
    await check_menu_eq_menu(async_client, answer)

    # созданное меню должно присутствовать в menus
    await check_menu_in_menus(async_client, answer)


@pytest.mark.asyncio
async def test_update_menu_and_check(db_test_data: AsyncSession, async_client: AsyncClient):
    # создаем меню
    menu_id = await create_menu(async_client, random_word(13), random_word(20))

    # изменяем на новые значения
    title = random_word(14)
    description = random_word(20)
    await patch_menu(async_client, menu_id, title, description)

    # ожидаемый ответ
    answer = {
        'id': menu_id,
        'title': title,
        'description': description,
        'submenus_count': 0,
        'dishes_count': 0,
    }

    # созданное меню должно вернуться при запросе меню по id
    await check_menu_eq_menu(async_client, answer)

    # созданное меню должно присутствовать в menus
    await check_menu_in_menus(async_client, answer)


@pytest.mark.asyncio
async def test_update_menu_duplicate(db_test_data: AsyncSession, async_client: AsyncClient):
    title = random_word(14)
    description = random_word(20)

    _ = await create_menu(async_client, title, description)
    menu_id2 = await create_menu(async_client, random_word(15), random_word(21))

    # изменяем на значения первого меню
    await patch_menu(async_client, menu_id2, title, description, waited_code=409)


@pytest.mark.asyncio
async def test_delete_menu_and_check(db_test_data: AsyncSession, async_client: AsyncClient):
    # create
    menu_id = await create_menu(async_client, random_word(18), random_word(20))

    # delete
    await delete_menu(async_client, menu_id)

    # re delete
    data = await delete_menu(async_client, menu_id, waited_code=404)
    assert data == {'detail': 'menu not found'}

    # check by menu_id
    await get_menu(async_client, menu_id, waited_code=404)

    # check in menus
    await check_menu_not_in_menus(async_client, menu_id)


@pytest.mark.asyncio
async def test_delete_menu_not_exist(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID_WRONG
    await delete_menu(async_client, menu_id, waited_code=404)
