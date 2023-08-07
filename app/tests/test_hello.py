import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_hello(async_client: AsyncClient):
    response = await async_client.get('/')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello World'}


@pytest.mark.asyncio
async def test_db_session(async_client: AsyncClient, async_db: AsyncSession):
    response = await async_client.get('/')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello World'}
