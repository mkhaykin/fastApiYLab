"""
    на момент теста у нас 2 записи по меню, 3 записи submenu и 3 записи dish
    00000000-0001-0000-0000-000000000000
        00000000-0000-0001-0000-000000000000
            00000000-0000-0000-0001-000000000000
            00000000-0000-0000-0002-000000000000
        00000000-0000-0002-0000-000000000000
            00000000-0000-0000-0003-000000000000
    00000000-0002-0000-0000-000000000000
        00000000-0000-0003-0000-000000000000
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.cache.actions import cache_get
from app.tests.utils import random_word


@pytest.mark.asyncio
async def test_menu_exist(db_create_dishes_clear_cache: AsyncSession, client: AsyncClient):
    response = await client.get('/api/v1/menus')
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = await client.get('/api/v1/menus/00000000-0001-0000-0000-000000000000')
    assert response.status_code == 200

    response = await client.get('/api/v1/menus/00000000-0002-0000-0000-000000000000')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_submenu_exist(db_create_dishes_clear_cache: AsyncSession, client: AsyncClient):
    response = await client.get('/api/v1/menus/00000000-0001-0000-0000-000000000000/submenus')
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = await client.get('/api/v1/menus/00000000-0002-0000-0000-000000000000/submenus')
    assert response.status_code == 200
    assert len(response.json()) == 1

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
async def test_dishes_exist(db_create_dishes_clear_cache: AsyncSession, client: AsyncClient):
    response = await client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0001-0000-000000000000/'
        'dishes'
    )
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = await client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0002-0000-000000000000/'
        'dishes'
    )
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = await client.get(
        '/api/v1/menus/00000000-0002-0000-0000-000000000000/'
        'submenus/00000000-0000-0003-0000-000000000000/'
        'dishes'
    )
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = await client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0001-0000-000000000000/'
        'dishes/00000000-0000-0000-0001-000000000000'
    )
    assert response.status_code == 200

    response = await client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0001-0000-000000000000/'
        'dishes/00000000-0000-0000-0002-000000000000'
    )
    assert response.status_code == 200

    response = await client.get(
        '/api/v1/menus/00000000-0001-0000-0000-000000000000/'
        'submenus/00000000-0000-0002-0000-000000000000/'
        'dishes/00000000-0000-0000-0003-000000000000'
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_start_counts(db_create_dishes_clear_cache: AsyncSession, client: AsyncClient):
    response = await client.get('/api/v1/menus/00000000-0001-0000-0000-000000000000')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 2
    assert response.json()['dishes_count'] == 3

    response = await client.get('/api/v1/menus/00000000-0002-0000-0000-000000000000')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 1
    assert response.json()['dishes_count'] == 0


@pytest.mark.asyncio
async def test_submenus_count(db_create_dishes_clear_cache: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    response = await client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    submenus_count = response.json()['submenus_count']
    dishes_count = response.json()['dishes_count']
    # create submenu
    response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus',
        json={
            'title': f'{random_word(10)}',
            'description': f'{random_word(20)}',
        },
    )
    assert response.status_code == 201
    submenu_id = response.json()['id']
    assert (await cache_get(menu_id, 'menu')) is None

    # check count: submenu + 1
    response = await client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == submenus_count + 1
    assert response.json()['dishes_count'] == dishes_count
    # delete submenu
    response = await client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    # check count: submenu back to start value
    response = await client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == submenus_count
    assert response.json()['dishes_count'] == dishes_count


@pytest.mark.asyncio
async def test_dishes_count(db_create_dishes_clear_cache: AsyncSession, client: AsyncClient):
    menu_id = '00000000-0001-0000-0000-000000000000'
    submenu_id = '00000000-0000-0001-0000-000000000000'
    response = await client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    submenus_count = response.json()['submenus_count']
    dishes_count = response.json()['dishes_count']
    # create dish
    response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json={
            'title': f'{random_word(10)}',
            'description': f'{random_word(20)}',
            'price': '1',
        },
    )
    assert response.status_code == 201
    dish_id = response.json()['id']
    # check count: submenu + 1
    response = await client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == submenus_count
    assert response.json()['dishes_count'] == dishes_count + 1
    # delete dish
    response = await client.delete(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    assert response.status_code == 200
    # check count: submenu start value
    response = await client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == submenus_count
    assert response.json()['dishes_count'] == dishes_count
