"""
Тест на то, что не ошибся в создании фикстуры с тестовыми данными
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_menu_exist(db_test_data: AsyncSession, async_client: AsyncClient):
    response = await async_client.get('/api/v1/menus')
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = await async_client.get('/api/v1/menus/00000000-0001-0000-0000-000000000000')
    assert response.status_code == 200

    response = await async_client.get('/api/v1/menus/00000000-0002-0000-0000-000000000000')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_submenu_exist(db_test_data: AsyncSession, async_client: AsyncClient):
    response = await async_client.get('/api/v1/menus/00000000-0001-0000-0000-000000000000/submenus')
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = await async_client.get('/api/v1/menus/00000000-0002-0000-0000-000000000000/submenus')
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = await async_client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0001-0000-000000000000'
    )
    assert response.status_code == 200
    response = await async_client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0002-0000-000000000000'
    )
    assert response.status_code == 200
    response = await async_client.get(
        '/api/v1/menus/00000000-0002-0000-0000-000000000000/'
        'submenus/00000000-0000-0003-0000-000000000000'
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_dishes_exist(db_test_data: AsyncSession, async_client: AsyncClient):
    response = await async_client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0001-0000-000000000000/'
        'dishes'
    )
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = await async_client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0002-0000-000000000000/'
        'dishes'
    )
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = await async_client.get(
        '/api/v1/menus/00000000-0002-0000-0000-000000000000/'
        'submenus/00000000-0000-0003-0000-000000000000/'
        'dishes'
    )
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = await async_client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0001-0000-000000000000/'
        'dishes/00000000-0000-0000-0001-000000000000'
    )
    assert response.status_code == 200

    response = await async_client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0001-0000-000000000000/'
        'dishes/00000000-0000-0000-0002-000000000000'
    )
    assert response.status_code == 200

    response = await async_client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0002-0000-000000000000/'
        'dishes/00000000-0000-0000-0003-000000000000'
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_dishes(db_test_data: AsyncSession, async_client: AsyncClient):
    response = await async_client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0001-0000-000000000000/dishes'
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_dish_not_found(db_test_data: AsyncSession, async_client: AsyncClient):
    response = await async_client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0001-0000-000000000000/'
        'dishes/00000000-0000-0000-9999-000000000000'
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}


@pytest.mark.asyncio
async def test_dish_not_found_wrong_submenu(db_test_data: AsyncSession, async_client: AsyncClient):
    response = await async_client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000002-0000-0000-0000-000000000000/'
        'dishes/00000000-0000-0000-0001-000000000000'
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_start_counts(db_test_data: AsyncSession, async_client: AsyncClient):
    response = await async_client.get('/api/v1/menus/00000000-0001-0000-0000-000000000000')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 2
    assert response.json()['dishes_count'] == 3

    response = await async_client.get('/api/v1/menus/00000000-0002-0000-0000-000000000000')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 1
    assert response.json()['dishes_count'] == 0
