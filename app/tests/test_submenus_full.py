import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.test_data import MENU_ID1


@pytest.mark.asyncio
async def test_submenus_full(db_test_data: AsyncSession, async_client: AsyncClient):
    menu_id = MENU_ID1
    response = await async_client.get(f'/api/v1/menus/{menu_id}/full')
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2

    # TODO check data
