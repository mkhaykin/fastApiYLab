import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.test_data import (
    DISH1,
    DISH2,
    DISH3,
    DISH_ID111,
    DISH_ID123,
    DISH_ID_WRONG,
    MENU_ID1,
    MENU_ID2,
    MENU_ID_WRONG,
    SUBMENU_ID11,
    SUBMENU_ID12,
    SUBMENU_ID23,
    SUBMENU_ID_WRONG,
)
from app.tests.test_utils import dict_in_list, random_word, round_price
from app.tests.test_utils_dish import (
    check_dish_eq_dish,
    check_dish_in_dishes,
    check_dish_not_exists,
    check_dish_not_in_dishes,
    create_dish,
    delete_dish,
    get_dish,
    get_dishes,
    patch_dish,
)


@pytest.mark.asyncio
async def test_dishes(db_test_data: AsyncSession, async_client: AsyncClient):
    data = await get_dishes(async_client, MENU_ID1, SUBMENU_ID11)
    assert len(data) == 2
    dict_in_list(DISH1, data)
    dict_in_list(DISH2, data)

    data = await get_dishes(async_client, MENU_ID1, SUBMENU_ID12)
    assert len(data) == 1
    dict_in_list(DISH3, data)


@pytest.mark.asyncio
async def test_dish(db_test_data: AsyncSession, async_client: AsyncClient):
    data = await get_dish(async_client, MENU_ID1, SUBMENU_ID11, DISH_ID111)
    await check_dish_eq_dish(async_client, MENU_ID1, data)


@pytest.mark.asyncio
async def test_dish_menu_not_exists(db_test_data: AsyncSession, async_client: AsyncClient):
    data = await get_dish(async_client, MENU_ID_WRONG, SUBMENU_ID11, DISH_ID111, waited_code=404)
    assert data == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_dish_submenu_not_exists(db_test_data: AsyncSession, async_client: AsyncClient):
    data = await get_dish(async_client, MENU_ID1, SUBMENU_ID_WRONG, DISH_ID111, waited_code=404)
    assert data == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_dish_dish_not_exists(db_test_data: AsyncSession, async_client: AsyncClient):
    data = await get_dish(async_client, MENU_ID1, SUBMENU_ID11, DISH_ID_WRONG, waited_code=404)
    assert data == {'detail': 'dish not found'}


@pytest.mark.asyncio
async def test_dish_wrong_menu(db_test_data: AsyncSession, async_client: AsyncClient):
    # Блюдо существует для подменю, но передаем не тот ID меню
    data = await get_dish(async_client, MENU_ID2, SUBMENU_ID11, DISH_ID111, waited_code=404)
    assert data == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_dish_wrong_submenu(db_test_data: AsyncSession, async_client: AsyncClient):
    # Подменю и меню переданы корректно, блюдо существует, но привязано к другому подменю
    data = await get_dish(async_client, MENU_ID1, SUBMENU_ID12, DISH_ID111, waited_code=404)
    assert data == {'detail': 'dish not found'}


@pytest.mark.asyncio
async def test_create_dishes_fix(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11
    await create_dish(
        async_client,
        menu_id,
        submenu_id,
        title='Dishes fixed',
        description='Dishes fixed description',
        price='1.0',
    )


@pytest.mark.asyncio
async def test_create_dish(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11
    title = random_word(10)
    description = random_word(20)
    price = '1.0'
    await create_dish(async_client, menu_id, submenu_id, title, description, price)


@pytest.mark.asyncio
async def test_create_dish_duplicate(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11
    title = random_word(7)
    description = random_word(20)
    price = '2.0'
    await create_dish(async_client, menu_id, submenu_id, title, description, price)
    await create_dish(async_client, menu_id, submenu_id, title, description, price, waited_code=409)


@pytest.mark.asyncio
async def test_create_dish_duplicate_another_submenu(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11
    title = random_word(8)
    description = random_word(20)
    price = '2.0'
    await create_dish(async_client, menu_id, submenu_id, title, description, price)

    submenu_id = SUBMENU_ID12
    await create_dish(async_client, menu_id, submenu_id, title, description, price, waited_code=409)


@pytest.mark.asyncio
async def test_create_dish_duplicate_another_menu(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11
    title = random_word(9)
    description = random_word(20)
    price = '2.0'
    await create_dish(async_client, menu_id, submenu_id, title, description, price)

    menu_id = MENU_ID2
    submenu_id = SUBMENU_ID23
    await create_dish(async_client, menu_id, submenu_id, title, description, price, waited_code=409)


@pytest.mark.asyncio
async def test_create_dish_duplicate_submenu_menu_wrong(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11
    title = random_word(9)
    description = random_word(20)
    price = '2.0'

    await create_dish(async_client, menu_id, submenu_id, title, description, price)

    # Пытаемся создать дубль для подменю, привязанного к другому меню. Должны получить 404, не 409!
    menu_id = MENU_ID2
    submenu_id = SUBMENU_ID11
    data = await create_dish(async_client, menu_id, submenu_id, title, description, price, waited_code=404)
    assert data == {'detail': 'submenu not found'}

    # аналогично для того же меню, что и создавалось, но подменю привязано к другому меню
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID23
    data = await create_dish(async_client, menu_id, submenu_id, title, description, price, waited_code=404)
    assert data == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_create_dish_duplicate_submenu_not_exist(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11
    title = random_word(9)
    description = random_word(20)
    price = '2.0'

    await create_dish(async_client, menu_id, submenu_id, title, description, price)

    # Пытаемся создать дубль для несуществующего подменю. Должны получить 404, не 409!
    menu_id = MENU_ID2
    submenu_id = SUBMENU_ID_WRONG
    data = await create_dish(async_client, menu_id, submenu_id, title, description, price, waited_code=404)
    assert data == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_create_dish_duplicate_menu_not_exist(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11
    title = random_word(9)
    description = random_word(20)
    price = '2.0'

    await create_dish(async_client, menu_id, submenu_id, title, description, price)

    # Пытаемся создать дубль с несуществующим меню, должны получить 404, не 409!
    menu_id = MENU_ID_WRONG
    submenu_id = SUBMENU_ID11
    data = await create_dish(async_client, menu_id, submenu_id, title, description, price, waited_code=404)
    assert data == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_create_dish_submenu_not_exist(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID_WRONG
    data = await create_dish(async_client, menu_id, submenu_id, random_word(10), random_word(20), '1',
                             waited_code=404)
    assert data == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_create_dish_menu_not_exist(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID_WRONG
    submenu_id = SUBMENU_ID11
    data = await create_dish(async_client, menu_id, submenu_id, random_word(10), random_word(20), '1',
                             waited_code=404)
    assert data == {'detail': 'menu not found'}


@pytest.mark.asyncio
@pytest.mark.parametrize('price', ('123', '10.22', '10.123', '10.126'))
async def test_create_dish_prices(db_test_data: AsyncSession, async_client: AsyncClient, price):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11
    title = random_word(10)
    description = random_word(20)
    await create_dish(async_client, menu_id, submenu_id, title, description, price)


@pytest.mark.asyncio
async def test_create_dish_and_check(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11

    # create
    title = random_word(11)
    description = random_word(20)
    price = '1.11'
    dish_id = await create_dish(async_client, menu_id, submenu_id, title, description, price)

    answer = {
        'id': dish_id,
        'submenu_id': submenu_id,
        'title': title,
        'description': description,
        'price': price,
    }

    # get dish by id
    await check_dish_eq_dish(async_client, menu_id, answer)

    # get all dishes
    await check_dish_in_dishes(async_client, menu_id, answer)


@pytest.mark.asyncio
async def test_update_dish_and_check(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11

    # create
    price = round_price('1')
    dish_id = await create_dish(async_client, menu_id, submenu_id, random_word(12), random_word(20), price)

    # patch with new values
    title = random_word(13)
    description = random_word(20)
    await patch_dish(async_client, menu_id, submenu_id, dish_id, title, description, price)

    answer = {
        'id': dish_id,
        'submenu_id': submenu_id,
        'title': title,
        'description': description,
        'price': price,
    }

    # get dish by id
    await check_dish_eq_dish(async_client, menu_id, answer)

    # get all dish
    await check_dish_in_dishes(async_client, menu_id, answer)


@pytest.mark.asyncio
async def test_update_dish_not_exists(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11
    dish_id = DISH_ID_WRONG

    title = random_word(13)
    description = random_word(20)
    price = round_price('1')

    data = await patch_dish(async_client, menu_id, submenu_id, dish_id, title, description, price, waited_code=404)
    assert data == {'detail': 'dish not found'}

    # блюдо не должно появиться
    await check_dish_not_exists(async_client, dish_id)


@pytest.mark.asyncio
async def test_delete_dish_and_check(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11

    # create
    title = random_word(13)
    description = random_word(20)
    price = '1'
    dish_id = await create_dish(async_client, menu_id, submenu_id, title, description, price)

    # delete
    await delete_dish(async_client, menu_id, submenu_id, dish_id)

    # re delete
    await delete_dish(async_client, menu_id, submenu_id, dish_id, waited_code=404)

    # get submenu by id
    await get_dish(async_client, menu_id, submenu_id, dish_id, waited_code=404)

    # get not in submenus for menu_id
    await check_dish_not_in_dishes(async_client, menu_id, submenu_id, dish_id)

    # check in all menus!
    await check_dish_not_exists(async_client, dish_id)


@pytest.mark.asyncio
async def test_delete_dish_dish_not_exist(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID11
    dish_id = DISH_ID_WRONG
    data = await delete_dish(async_client, menu_id, submenu_id, dish_id, waited_code=404)
    assert data == {'detail': 'dish not found'}


@pytest.mark.asyncio
async def test_delete_dish_submenu_not_exist(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    submenu_id = SUBMENU_ID_WRONG
    dish_id = DISH_ID111
    data = await delete_dish(async_client, menu_id, submenu_id, dish_id, waited_code=404)
    assert data == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_delete_dish_menu_not_exist(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID_WRONG
    submenu_id = SUBMENU_ID11
    dish_id = DISH_ID111
    data = await delete_dish(async_client, menu_id, submenu_id, dish_id, waited_code=404)
    assert data == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_delete_dish_wrong_submenu(db_test_data: AsyncSession, async_client: AsyncClient):
    # Блюдо существует для подменю, но передаем не тот ID меню
    data = await delete_dish(async_client, MENU_ID2, SUBMENU_ID11, DISH_ID111, waited_code=404)
    assert data == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_delete_dish_wrong_dish(db_test_data: AsyncSession, async_client: AsyncClient):
    # Подменю и меню переданы корректно, блюдо существует, но привязано к другому подменю
    data = await delete_dish(async_client, MENU_ID1, SUBMENU_ID11, DISH_ID123, waited_code=404)
    assert data == {'detail': 'dish not found'}
