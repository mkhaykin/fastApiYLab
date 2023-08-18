"""
    Проверка на передачу не корректных id в json запроса (не в URL)
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.test_data import MENU_ID_WRONG
from app.tests.test_utils import compare_response, random_word
from app.tests.test_utils_menu import check_menu_in_menus, check_menu_not_in_menus


@pytest.mark.asyncio
async def test_wrong_id_in_json(async_db: AsyncSession, async_client: AsyncClient):
    """
     Переданный id в меню должен игнорироваться
    :param async_db:
    :param async_client:
    :return:
    """
    wrong_id: str = MENU_ID_WRONG
    title: str = random_word(10)
    description: str = random_word(20)

    response = await async_client.post(
        '/api/v1/menus',
        json={
            'id': wrong_id,  # вот это должны проигнорировать!
            'title': f'{title}',
            'description': f'{description}',
        },
    )
    assert response.status_code == 201
    menu_id: str = response.json()['id']
    assert menu_id != wrong_id

    answer: dict[str, str | int] = {
        'id': menu_id,
        'title': title,
        'description': description,
    }

    assert compare_response(answer=response.json(), expected_answer=answer)

    await check_menu_in_menus(async_client, answer)

    await check_menu_not_in_menus(async_client, wrong_id)
