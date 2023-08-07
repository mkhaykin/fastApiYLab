"""
    Тестирование прод базы.
    Только проверка api.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_alive(db_prod: AsyncSession, client: AsyncClient):
    response = await client.get('/')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello World'}


@pytest.mark.asyncio
async def test_menus(db_prod: AsyncSession, client: AsyncClient):
    response = await client.get('/api/v1/menus')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_submenus(db_prod: AsyncSession, client: AsyncClient):
    response = await client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000/submenus')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_dishes(db_prod: AsyncSession, client: AsyncClient):
    response = await client.get(
        '/api/v1/menus/00000000-0000-0000-0000-000000000000/submenus/00000000-0000-0000-0000-000000000000/dishes'
    )
    assert response.status_code == 200
