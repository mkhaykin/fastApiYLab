"""
    на момент теста у нас 2 записи по меню
    00000000-0001-0000-0000-000000000000
    00000000-0002-0000-0000-000000000000
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.utils import random_word
from app.tests.utils_submenu import (  # get_submenu,
    check_submenu_eq_submenu,
    check_submenu_in_submenus,
    check_submenu_not_in_submenus,
    create_submenu,
    patch_submenu,
)


@pytest.mark.asyncio
async def test_menu_exist(db_create_menus: AsyncSession, async_client: AsyncClient):
    response = await async_client.get('/api/v1/menus/00000000-0001-0000-0000-000000000000')
    assert response.status_code == 200
    response = await async_client.get('/api/v1/menus/00000000-0002-0000-0000-000000000000')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_submenus(db_create_menus: AsyncSession, async_client: AsyncClient):
    response = await async_client.get('/api/v1/menus/00000000-0001-0000-0000-000000000000/submenus')
    assert response.status_code == 200
    assert not response.json()


@pytest.mark.asyncio
async def test_submenu_not_found(db_create_menus: AsyncSession, client: AsyncClient):
    # TODO перенести в отдельный блок тестов. При перемешанном тестировании субменю может существовать ...
    response = await client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/submenus/00000000-0000-0000-0000-000000000000'
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_create_submenu_fix(db_create_menus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    await create_submenu(
        client, menu_id, title='Submenu 1', description='Submenu 1 description'
    )


@pytest.mark.asyncio
async def test_create_submenu_duplicate(db_create_menus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    await create_submenu(
        client, menu_id, title='Submenu 2', description='Submenu 2 description'
    )
    response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus',
        json={'title': 'Submenu 2', 'description': 'Submenu 2 description'},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_submenu_duplicate_another_submenu(db_create_menus: AsyncSession, client: AsyncClient):
    # перенести в отдельную проверку дублей, т.к. опять завязано на верхнем тесте
    menu_id = '00000000-0001-0000-0000-000000000000'
    response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus',
        json={'title': 'Submenu 1', 'description': 'Submenu 1 description'},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_submenu_menu_not_exist(db_create_menus: AsyncSession, client: AsyncClient):
    menu_id = '00000001-0000-0000-0000-000000000000'
    response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus',
        json={'title': 'Submenu ...', 'description': 'Submenu ... description'},
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_create_submenu(db_create_menus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    title = random_word(10)
    description = random_word(20)
    await create_submenu(client, menu_id, title, description)


@pytest.mark.asyncio
async def test_create_submenu_and_check(db_create_menus: AsyncSession, client: AsyncClient):
    # TODO оформить создание и проверку в утилиты.
    # create
    menu_id = '00000000-0001-0000-0000-000000000000'
    title = random_word(11)
    description = random_word(20)
    submenu_id = await create_submenu(client, menu_id, title, description)

    answer = {
        'id': submenu_id,
        'menu_id': menu_id,
        'title': title,
        'description': description,
        # 'dishes_count': 0,
    }
    # get submenu by id
    # data = await get_submenu(client, menu_id, submenu_id)
    # assert data == answer
    await check_submenu_eq_submenu(client, answer)

    # get all submenus
    await check_submenu_in_submenus(client, answer)


@pytest.mark.asyncio
async def test_update_submenu_and_check(db_create_menus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    # create
    submenu_id = await create_submenu(client, menu_id, random_word(12), random_word(20))

    # patch with new values
    title = random_word(13)
    description = random_word(20)
    await patch_submenu(client, menu_id, submenu_id, title, description)

    answer = {
        'id': submenu_id,
        'menu_id': menu_id,
        'title': title,
        'description': description,
        # 'dishes_count': 0,
    }
    # get submenu by id
    await check_submenu_eq_submenu(client, answer)

    # get all submenus
    await check_submenu_in_submenus(client, answer)


@pytest.mark.asyncio
async def test_delete_submenu_and_check(db_create_menus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    # create
    submenu_id = await create_submenu(client, menu_id, random_word(14), random_word(20))

    # delete
    response = await client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200

    # get submenu by id
    response = await client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 404

    # check all submenus in menu
    await check_submenu_not_in_submenus(client, menu_id, submenu_id)

    # check all menus
    response = await client.get('/api/v1/menus')
    menus = response.json()
    for menu in menus:
        await check_submenu_not_in_submenus(client, menu['id'], submenu_id)


@pytest.mark.asyncio
async def test_delete_submenu_not_exist(db_create_menus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-999999999999'

    response = await client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_delete_submenu_menu_not_exist(db_create_menus: AsyncSession, client: AsyncClient):
    # create
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = await create_submenu(client, menu_id, random_word(14), random_word(20))
    # delete from another menu
    menu_id = '00000000-0001-0000-0000-999999999999'
    response = await client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_delete_submenu_menu_and_submenu_not_exist(db_create_menus: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-999999999999'
    submenu_id = '00000000-0000-0001-0000-999999999999'
    response = await client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}
