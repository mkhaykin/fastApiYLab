"""
    проверка на передачу не корректных id в json запроса (не в URL)
"""
from app.tests.utils import random_word
from app.tests.utils_menu import (  # check_menu_eq_menu,; create_menu,; get_menu,; patch_menu,
    check_menu_in_menus,
    check_menu_not_in_menus,
)


def test_wrong_id_in_json(db_test, client):
    """
    переданный id в меню должен игнорироваться
    :param db_test:
    :param client:
    :return:
    """
    wrong_id: str = '00000000-0000-0000-0000-000000000000'
    title = random_word(10)
    description = random_word(20)

    response = client.post(
        '/api/v1/menus',
        json={
            'id': wrong_id,
            'title': f'{title}',
            'description': f'{description}',
        },
    )
    assert response.status_code == 201
    menu_id: str = response.json()['id']

    answer = {
        'id': menu_id,
        'title': title,
        'description': description,
        'submenus_count': 0,
        'dishes_count': 0,
    }
    assert response.json() == answer
    check_menu_in_menus(client, answer)
    check_menu_not_in_menus(client, wrong_id)
