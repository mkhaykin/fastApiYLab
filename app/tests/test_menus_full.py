import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.test_utils_dish import get_dishes
from app.tests.test_utils_menu import get_menus
from app.tests.test_utils_submenu import get_submenus


async def _get_flat_data(async_client: AsyncClient):
    flat_data = []
    menus = await get_menus(async_client)
    for menu in menus:
        item = {
            'menu_id': menu['id'],
            'menu_title': menu['title'],
            'menu_description': menu['description'],
            'menu_submenus_count': menu['submenus_count'],
            'menu_dishes_count': menu['dishes_count'],
            'submenu_id': None,
            'submenu_title': None,
            'submenu_description': None,
            'dishes_in_submenu_count': None,
            'dish_id': None,
            'dish_title': None,
            'dish_description': None,
            'dish_price': None,
        }
        submenus = await get_submenus(async_client, menu['id'])
        for submenu in submenus:
            item.update({
                'submenu_id': submenu['id'],
                'submenu_title': submenu['title'],
                'submenu_description': submenu['description'],
                'dishes_in_submenu_count': submenu['dishes_count'],
                'dish_id': None,
                'dish_title': None,
                'dish_description': None,
                'dish_price': None,
            })
            dishes = await get_dishes(async_client, menu['id'], submenu['id'])
            for dish in dishes:
                item.update({
                    'dish_id': dish['id'],
                    'dish_title': dish['title'],
                    'dish_description': dish['description'],
                    'dish_price': dish['price'],
                })
                flat_data.append(item)
            if not dishes:
                flat_data.append(item)
        if not submenus:
            flat_data.append(item)

    return flat_data


@pytest.mark.asyncio
async def test_menus_orm_all(db_test_data: AsyncSession, async_client: AsyncClient):
    response = await async_client.get('/all')
    assert response.status_code == 200
    assert response.json()

    data = response.json()
    flat_data = await _get_flat_data(async_client)

    assert len(flat_data) == len(data)

    for item in flat_data:
        assert item in data


@pytest.mark.asyncio
async def test_menus_full(db_test_data: AsyncSession, async_client: AsyncClient):
    response = await async_client.get('/api/v1/full')
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2

    # TODO check data
