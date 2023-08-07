import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.utils import random_word
from app.tests.utils_menu import (
    check_menu_eq_menu,
    check_menu_in_menus,
    check_menu_not_in_menus,
    create_menu,
    patch_menu,
)


@pytest.mark.asyncio
async def test_menus(async_db: AsyncSession, async_client: AsyncClient):
    response = await async_client.get('/api/v1/menus')
    assert response.status_code == 200
    assert not response.json()    # data must be cleared for this test


@pytest.mark.asyncio
async def test_menu_not_found(async_db: AsyncSession, async_client: AsyncClient):
    response = await async_client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_create_menu_fix(async_db: AsyncSession, async_client: AsyncClient):
    await create_menu(async_client, 'My menu 1', 'My menu description 1')


@pytest.mark.asyncio
async def test_create_menu_duplicate(async_db: AsyncSession, async_client: AsyncClient):
    title, description = 'My menu 2', 'My menu description 2'
    await create_menu(async_client, title, description)
    response = await async_client.post(
        '/api/v1/menus',
        json={'title': title, 'description': description},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_menu_random(async_db: AsyncSession, async_client: AsyncClient):
    title = random_word(10)
    description = random_word(20)
    await create_menu(async_client, title, description)


@pytest.mark.asyncio
async def test_create_menu_and_find_it(async_db: AsyncSession, async_client: AsyncClient):
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
    await check_menu_eq_menu(async_client, answer)


@pytest.mark.asyncio
async def test_create_menu_and_find_it_in_menus(async_db: AsyncSession, async_client: AsyncClient):
    # create
    title = random_word(12)
    description = random_word(20)
    menu_id = await create_menu(async_client, title, description)

    # check
    answer = {
        'id': menu_id,
        'title': title,
        'description': description,
        'submenus_count': 0,
        'dishes_count': 0,
    }
    await check_menu_in_menus(async_client, answer)


@pytest.mark.asyncio
async def test_update_menu_and_find_it(async_db: AsyncSession, async_client: AsyncClient):
    # create menu
    menu_id = await create_menu(async_client, random_word(13), random_word(20))
    # patch with new values
    title = random_word(14)
    description = random_word(20)
    _ = await patch_menu(async_client, menu_id, title, description)

    # check
    answer = {
        'id': menu_id,
        'title': title,
        'description': description,
        'submenus_count': 0,
        'dishes_count': 0,
    }
    _ = await check_menu_eq_menu(async_client, answer)


@pytest.mark.asyncio
async def test_update_menu_and_find_it_in_menus(async_db: AsyncSession, async_client: AsyncClient):
    menu_id = await create_menu(async_client, random_word(15), random_word(20))
    # patch with new values
    title = random_word(16)
    description = random_word(20)
    await patch_menu(async_client, menu_id, title, description)

    # check
    answer = {
        'id': menu_id,
        'title': title,
        'description': description,
        'submenus_count': 0,
        'dishes_count': 0,
    }
    await check_menu_eq_menu(async_client, answer)


@pytest.mark.asyncio
async def test_delete_menu(async_db: AsyncSession, async_client: AsyncClient):
    menu_id = await create_menu(async_client, random_word(17), random_word(20))
    response = await async_client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_menu_not_exist(async_db: AsyncSession, async_client: AsyncClient):
    menu_id = '00000000-0000-0000-0000-000000000000'
    response = await async_client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_menu_and_check(async_db: AsyncSession, async_client: AsyncClient):
    # create
    menu_id = await create_menu(async_client, random_word(18), random_word(20))
    # delete
    response = await async_client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    # check by menu_id
    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}
    # check in menus
    await check_menu_not_in_menus(async_client, menu_id)
