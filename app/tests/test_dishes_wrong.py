"""
    Проверка на передачу не корректных id в json запроса (не в URL)
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.test_data import DISH_ID_WRONG, MENU_ID1, SUBMENU_ID11, SUBMENU_ID_WRONG
from app.tests.test_utils import random_word
from app.tests.test_utils_dish import check_dish_not_exists


@pytest.mark.asyncio
async def test_dish_wrong_ids_in_json(db_test_data: AsyncSession, async_client: AsyncClient):
    """
     Переданный id в блюде должен игнорироваться
    :param async_db:
    :param async_client:
    :return:
    """
    menu_id: str = MENU_ID1
    submenu_id: str = SUBMENU_ID11
    wrong_dish_id: str = DISH_ID_WRONG
    wrong_dish_submenu_id: str = SUBMENU_ID_WRONG

    title: str = random_word(10)
    description: str = random_word(20)

    response = await async_client.post(
        url=f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json={
            'id': wrong_dish_id,  # вот это должны проигнорировать!
            'submenu_id': wrong_dish_submenu_id,  # и вот это тоже!
            'title': f'{title}',
            'description': f'{description}',
            'price': '1.11',
        },
    )
    assert response.status_code == 201
    dish_id = response.json()['id']
    submenu_id = response.json()['submenu_id']

    assert dish_id != wrong_dish_id
    assert submenu_id != wrong_dish_submenu_id

    # Проверяем на артефакты:
    # не должно нигде появиться блюдо с wrong_dish_id
    await check_dish_not_exists(async_client, wrong_dish_id)
