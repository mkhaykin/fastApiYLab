"""
    проверка на передачу не корректных id в json запроса (не в URL)
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.utils import random_word
from app.tests.utils_menu import (  # check_menu_eq_menu,; create_menu,; get_menu,; patch_menu,
    check_menu_in_menus,
    check_menu_not_in_menus,
)


@pytest.mark.asyncio
async def test_wrong_id_in_json(async_db: AsyncSession, client: AsyncClient):
    """
    переданный id в меню должен игнорироваться
    :param async_db:
    :param client:
    :return:
    """
    wrong_id: str = '00000000-0000-0000-0000-000000000000'
    title: str = random_word(10)
    description: str = random_word(20)

    response = await client.post(
        '/api/v1/menus',
        json={
            'id': wrong_id,
            'title': f'{title}',
            'description': f'{description}',
        },
    )
    assert response.status_code == 201
    menu_id: str = response.json()['id']

    answer: dict[str, str | int] = {
        'id': menu_id,
        'title': title,
        'description': description,
        # 'submenus_count': 0,
        # 'dishes_count': 0,
    }
    assert response.json() == answer
    answer = {
        'id': menu_id,
        'title': title,
        'description': description,
        'submenus_count': 0,
        'dishes_count': 0,
    }
    await check_menu_in_menus(client, answer)
    await check_menu_not_in_menus(client, wrong_id)
