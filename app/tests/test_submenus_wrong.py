"""
    Проверка на передачу не корректных id в json запроса (не в URL)
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.test_data import DISH_ID_WRONG, MENU_ID1
from app.tests.test_utils import random_word
from app.tests.test_utils_submenu import check_submenu_not_exists


@pytest.mark.asyncio
async def test_submenus_wrong_ids_in_json(db_test_data: AsyncSession, async_client: AsyncClient):
    """
     Переданный id в блюде должен игнорироваться
    :param db_test_data:
    :param async_client:
    :return:
    """
    menu_id: str = MENU_ID1
    wrong_submenu_id: str = DISH_ID_WRONG
    wrong_submenu_menu_id: str = DISH_ID_WRONG

    title: str = random_word(10)
    description: str = random_word(20)

    response = await async_client.post(
        url=f'/api/v1/menus/{menu_id}/submenus',
        json={
            'id': wrong_submenu_id,  # вот это должны проигнорировать!
            'menu_id': wrong_submenu_menu_id,  # и вот это тоже!
            'title': f'{title}',
            'description': f'{description}',
        },
    )
    assert response.status_code == 201
    submenu_id: str = response.json()['id']
    menu_id = response.json()['menu_id']

    assert menu_id != wrong_submenu_id
    assert submenu_id != wrong_submenu_menu_id

    # Проверяем на артефакты:
    # не должно нигде появиться подменю с wrong_submenu_id
    await check_submenu_not_exists(async_client, wrong_submenu_id)
