"""
    на момент теста у нас 2 записи по меню и 3 записи submenu
    00000000-0001-0000-0000-000000000000
        00000000-0000-0001-0000-000000000000
        00000000-0000-0002-0000-000000000001
    00000000-0002-0000-0000-000000000001
        00000000-0000-0003-0000-000000000002
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.utils import random_word, round_price
from app.tests.utils_dish import (
    check_dish_eq_dish,
    check_dish_in_dishes,
    check_dish_not_in_dishes,
    create_dish,
    patch_dish,
)


@pytest.mark.asyncio
async def test_menu_exist(db_create_submenus: AsyncSession, client: AsyncClient):
    # проверка фикстуры
    response = await client.get('/api/v1/menus/00000000-0001-0000-0000-000000000000')
    assert response.status_code == 200
    response = await client.get('/api/v1/menus/00000000-0002-0000-0000-000000000000')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_submenu_exist(db_create_submenus: AsyncSession, client: AsyncClient):
    # проверка фикстуры
    response = await client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0001-0000-000000000000'
    )
    assert response.status_code == 200
    response = await client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0002-0000-000000000000'
    )
    assert response.status_code == 200
    response = await client.get(
        '/api/v1/menus/00000000-0002-0000-0000-000000000000/'
        'submenus/00000000-0000-0003-0000-000000000000'
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_dishes(db_create_submenus: AsyncSession, client: AsyncClient):
    response = await client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0001-0000-000000000000/dishes'
    )
    assert response.status_code == 200
    # assert not response.json()


@pytest.mark.asyncio
async def test_dish_not_found(db_create_submenus: AsyncSession, client: AsyncClient):
    response = await client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0001-0000-000000000000/'
        'dishes/00000000-0000-0000-0000-000000000000'
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}


@pytest.mark.asyncio
async def test_dish_not_found_wrong_submenu(db_create_submenus: AsyncSession, client: AsyncClient):
    response = await client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000002-0000-0000-0000-000000000000/'
        'dishes/00000000-0000-0000-0001-000000000000'
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_create_dishes_fix(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'

    await create_dish(
        client,
        menu_id,
        submenu_id,
        title='Dishes 1',
        description='Dishes 1 description',
        price='1.0',
    )


@pytest.mark.asyncio
async def test_create_dish_duplicate(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    title = random_word(7)
    description = random_word(20)
    price = '2.0'
    await create_dish(
        client,
        menu_id,
        submenu_id,
        title,
        description,
        price,
    )
    response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json={
            'title': title,
            'description': description,
            'price': price,
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_dish_duplicate_another_submenu(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    title = random_word(8)
    description = random_word(20)
    price = '2.0'
    await create_dish(
        client,
        menu_id,
        submenu_id,
        title,
        description,
        price,
    )
    response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json={
            'title': title,
            'description': description,
            'price': price,
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_dish_duplicate_another_menu(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    title = random_word(9)
    description = random_word(20)
    price = '2.0'
    await create_dish(
        client,
        menu_id,
        submenu_id,
        title,
        description,
        price,
    )

    menu_id = '00000000-0002-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json={
            'title': title,
            'description': description,
            'price': price,
        },
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_create_dish_submenu_not_exist(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-9999-0000-000000000000'
    response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json={
            'title': 'Dishes ...',
            'description': 'Dishes ... description',
            'price': '1',
        },
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_create_dish_menu_not_exist(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-9999-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json={
            'title': 'Dishes ...',
            'description': 'Dishes ... description',
            'price': '1',
        },
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_create_dish(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    title = random_word(10)
    description = random_word(20)
    price = '1.0'
    await create_dish(client, menu_id, submenu_id, title, description, price)


@pytest.mark.asyncio
async def test_create_dish_price_int(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    title = random_word(10)
    description = random_word(20)
    price = '123'
    await create_dish(client, menu_id, submenu_id, title, description, price)


@pytest.mark.asyncio
async def test_create_dish_price_float(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    title = random_word(5)
    description = random_word(20)
    price = '10.22'
    await create_dish(client, menu_id, submenu_id, title, description, price)


@pytest.mark.asyncio
async def test_create_dish_price_floor(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    title = random_word(6)
    description = random_word(20)
    price = '10.123'
    await create_dish(client, menu_id, submenu_id, title, description, price)


@pytest.mark.asyncio
async def test_create_dish_price_ceil(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    title = random_word(7)
    description = random_word(20)
    price = '10.126'
    await create_dish(client, menu_id, submenu_id, title, description, price)


@pytest.mark.asyncio
async def test_create_dish_and_check(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    # create
    title = random_word(11)
    description = random_word(20)
    price = '1.11'
    dish_id = await create_dish(client, menu_id, submenu_id, title, description, price)

    answer = {
        'id': dish_id,
        'submenu_id': submenu_id,
        'title': title,
        'description': description,
        'price': price,
    }

    # get dish by id
    await check_dish_eq_dish(client, menu_id, answer)

    # get all dishes
    await check_dish_in_dishes(client, menu_id, answer)


@pytest.mark.asyncio
async def test_update_dish_and_check(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    # create
    price = round_price('1')
    dish_id = await create_dish(client, menu_id, submenu_id, random_word(12), random_word(20), price)

    # patch with new values
    title = random_word(13)
    description = random_word(20)
    await patch_dish(client, menu_id, submenu_id, dish_id, title, description, price)

    answer = {
        'id': dish_id,
        'submenu_id': submenu_id,
        'title': title,
        'description': description,
        'price': price,
    }

    # get dish by id
    await check_dish_eq_dish(client, menu_id, answer)

    # get all dish
    await check_dish_in_dishes(client, menu_id, answer)


@pytest.mark.asyncio
async def test_delete_dish_and_check(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    # create
    title = random_word(13)
    description = random_word(20)
    price = '1'
    dish_id = await create_dish(client, menu_id, submenu_id, title, description, price)

    # delete
    response = await client.delete(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    assert response.status_code == 200

    # get submenu by id
    response = await client.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    assert response.status_code == 404

    # get all submenus
    await check_dish_not_in_dishes(client, menu_id, submenu_id, dish_id)

    # check all menus!
    menus = (await client.get('/api/v1/menus')).json()
    for menu in menus:
        submenus = (await client.get(f"/api/v1/menus/{menu['id']}/submenus")).json()
        for submenu in submenus:
            await check_dish_not_in_dishes(client, menu['id'], submenu['id'], dish_id)


@pytest.mark.asyncio
async def test_delete_submenu_not_exist(db_create_submenus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    dish_id = '00000000-0000-0000-0000-000000000000'
    response = await client.delete(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    assert response.status_code == 404
