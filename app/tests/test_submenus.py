import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.test_data import (
    MENU_ID1,
    MENU_ID2,
    MENU_ID_WRONG,
    SUBMENU1,
    SUBMENU2,
    SUBMENU3,
    SUBMENU_ID11,
    SUBMENU_ID_WRONG,
)
from app.tests.test_utils import compare_response, dict_in_list, random_word
from app.tests.test_utils_submenu import (
    check_submenu_eq_submenu,
    check_submenu_in_submenus,
    check_submenu_not_exists,
    check_submenu_not_in_submenus,
    create_submenu,
    delete_submenu,
    get_submenu,
    get_submenus,
    patch_submenu,
)


@pytest.mark.asyncio
async def test_submenus(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    data = await get_submenus(async_client, menu_id)
    assert len(data) == 2
    assert dict_in_list(SUBMENU1, data)
    assert dict_in_list(SUBMENU2, data)

    menu_id = MENU_ID2
    data = await get_submenus(async_client, menu_id)
    assert len(data) == 1
    assert dict_in_list(SUBMENU3, data)


@pytest.mark.asyncio
async def test_submenu(db_test_data: AsyncSession, async_client: AsyncClient):
    submenu = SUBMENU1
    data = await get_submenu(async_client, submenu['menu_id'], submenu['id'])
    compare_response(data, submenu)


@pytest.mark.asyncio
async def test_submenu_submenu_not_exists(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1  # меню существует
    submenu_id = SUBMENU_ID_WRONG  # подменю не существует
    data = await get_submenu(async_client, menu_id, submenu_id, waited_code=404)
    assert data == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_submenu_menu_not_exists(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID_WRONG  # меню не существует
    submenu_id = SUBMENU_ID11  # подменю существует
    data = await get_submenu(async_client, menu_id, submenu_id, waited_code=404)
    assert data == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_submenu_wrong_menu(db_test_data: AsyncSession, async_client: AsyncClient):
    # Подменю существует, но передаем не тот ID меню (тоже существующий)
    data = await get_submenu(async_client, MENU_ID2, SUBMENU_ID11, waited_code=404)
    assert data == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_create_submenu_fix(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    await create_submenu(async_client, menu_id, 'Submenu 1 fixed', 'Submenu 1 fixed description')


@pytest.mark.asyncio
async def test_create_submenu(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    title = random_word(10)
    description = random_word(20)
    await create_submenu(async_client, menu_id, title, description)


@pytest.mark.asyncio
async def test_create_submenu_duplicate(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    title = random_word(10)
    description = random_word(20)
    await create_submenu(async_client, menu_id, title, description)
    await create_submenu(async_client, menu_id, title, description, waited_code=409)


@pytest.mark.asyncio
async def test_create_submenu_duplicate_another_submenu(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id1 = MENU_ID1
    menu_id2 = MENU_ID2
    title = random_word(10)
    description = random_word(20)
    await create_submenu(async_client, menu_id1, title, description)
    await create_submenu(async_client, menu_id2, title, description, waited_code=409)


@pytest.mark.asyncio
async def test_create_submenu_duplicate_menu_not_exists(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID_WRONG
    title = random_word(10)
    description = random_word(20)
    data = await create_submenu(async_client, menu_id, title, description, waited_code=404)
    assert data == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_create_submenu_and_check(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    title = random_word(11)
    description = random_word(20)

    # create
    submenu_id = await create_submenu(async_client, menu_id, title, description)

    answer = {
        'id': submenu_id,
        'menu_id': menu_id,
        'title': title,
        'description': description,
        'dishes_count': 0,
    }

    # созданное меню должно вернуться при запросе подменю по id
    await check_submenu_eq_submenu(async_client, answer)

    # созданное меню должно вернуться при запросе всех подменю
    await check_submenu_in_submenus(async_client, answer)


@pytest.mark.asyncio
async def test_update_submenu_and_check(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1

    # create
    submenu_id = await create_submenu(async_client, menu_id, random_word(12), random_word(20))

    # patch with new values
    title = random_word(13)
    description = random_word(20)
    await patch_submenu(async_client, menu_id, submenu_id, title, description)

    answer = {
        'id': submenu_id,
        'menu_id': menu_id,
        'title': title,
        'description': description,
        'dishes_count': 0,
    }

    # get submenu by id
    await check_submenu_eq_submenu(async_client, answer)

    # get all submenus
    await check_submenu_in_submenus(async_client, answer)


@pytest.mark.asyncio
async def test_update_submenu_not_exists(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID_WRONG

    title = random_word(13)
    description = random_word(20)

    data = await patch_submenu(async_client, menu_id, submenu_id, title, description, waited_code=404)
    assert data == {'detail': 'submenu not found'}

    # блюдо не должно появиться
    await check_submenu_not_exists(async_client, submenu_id)


@pytest.mark.asyncio
async def test_delete_submenu_and_check(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1

    # create
    submenu_id = await create_submenu(async_client, menu_id, random_word(14), random_word(20))

    # delete
    await delete_submenu(async_client, menu_id, submenu_id)

    # re delete
    data = await delete_submenu(async_client, menu_id, submenu_id, waited_code=404)
    assert data == {'detail': 'submenu not found'}

    # get submenu by id
    await get_submenu(async_client, menu_id, submenu_id, waited_code=404)

    # check all submenus in menu
    await check_submenu_not_in_submenus(async_client, menu_id, submenu_id)

    # check all menus
    await check_submenu_not_exists(async_client, submenu_id)


@pytest.mark.asyncio
async def test_delete_submenu_not_exist(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID_WRONG

    data = await delete_submenu(async_client, menu_id, submenu_id, waited_code=404)
    assert data == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_delete_submenu_menu_not_exist(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID_WRONG
    submenu_id = SUBMENU_ID11

    data = await delete_submenu(async_client, menu_id, submenu_id, waited_code=404)
    assert data == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_delete_submenu_menu_and_submenu_not_exist(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID_WRONG
    submenu_id = SUBMENU_ID_WRONG

    data = await delete_submenu(async_client, menu_id, submenu_id, waited_code=404)
    assert data == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_delete_submenu_wrong_submenu(db_test_data: AsyncSession, async_client: AsyncClient):
    # Подменю существует, но относится к другому меню
    data = await delete_submenu(async_client, MENU_ID2, SUBMENU_ID11, waited_code=404)
    assert data == {'detail': 'submenu not found'}
