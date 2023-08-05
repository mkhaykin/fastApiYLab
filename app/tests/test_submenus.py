"""
    на момент теста у нас 2 записи по меню
    00000000-0000-0000-0000-000000000000
    00000000-0000-0000-0000-000000000001
"""
from sqlalchemy.orm.session import Session
from starlette.testclient import TestClient

from app.tests.utils import random_word
from app.tests.utils_submenu import (
    check_submenu_eq_submenu,
    check_submenu_in_submenus,
    check_submenu_not_in_submenus,
    create_submenu,
    get_submenu,
    patch_submenu,
)


def test_menu_exist(db_create_menus: Session, client: TestClient):
    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 200
    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000001')
    assert response.status_code == 200


def test_submenus(db_create_menus: Session, client: TestClient):
    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000/submenus')
    assert response.status_code == 200
    assert not response.json()


def test_submenu_not_found(db_create_menus: Session, client: TestClient):
    # TODO перенести в отдельный блок тестов. При перемешанном тестировании субменю может существовать ...
    response = client.get(
        '/api/v1/menus/00000000-0000-0000-0000-000000000000/submenus/00000000-0000-0000-0000-000000000000'
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


def test_create_submenu_fix(db_create_menus: Session, client: TestClient):
    menu_id = '00000000-0000-0000-0000-000000000000'
    create_submenu(
        client, menu_id, title='Submenu 1', description='Submenu 1 description'
    )


def test_create_submenu_duplicate(db_create_menus: Session, client: TestClient):
    menu_id = '00000000-0000-0000-0000-000000000000'
    create_submenu(
        client, menu_id, title='Submenu 2', description='Submenu 2 description'
    )
    response = client.post(
        f'/api/v1/menus/{menu_id}/submenus',
        json={'title': 'Submenu 2', 'description': 'Submenu 2 description'},
    )
    assert response.status_code == 409


def test_create_submenu_duplicate_another_submenu(db_create_menus: Session, client: TestClient):
    # перенести в отдельную проверку дублей, т.к. опять завязано на верхнем тесте
    menu_id = '00000000-0000-0000-0000-000000000001'
    response = client.post(
        f'/api/v1/menus/{menu_id}/submenus',
        json={'title': 'Submenu 1', 'description': 'Submenu 1 description'},
    )
    assert response.status_code == 409


def test_create_submenu_menu_not_exist(db_create_menus: Session, client: TestClient):
    menu_id = '00000000-0000-0000-0000-000000000002'
    response = client.post(
        f'/api/v1/menus/{menu_id}/submenus',
        json={'title': 'Submenu ...', 'description': 'Submenu ... description'},
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}


def test_create_submenu(db_create_menus: Session, client: TestClient):
    menu_id = '00000000-0000-0000-0000-000000000000'
    title = random_word(10)
    description = random_word(20)
    create_submenu(client, menu_id, title, description)


def test_create_submenu_and_check(db_create_menus: Session, client: TestClient):
    # create
    menu_id = '00000000-0000-0000-0000-000000000001'
    title = random_word(11)
    description = random_word(20)
    submenu_id = create_submenu(client, menu_id, title, description)

    answer = {
        'id': submenu_id,
        'menu_id': menu_id,
        'title': title,
        'description': description,
        'dishes_count': 0,
    }
    # get submenu by id
    data = get_submenu(client, menu_id, submenu_id)
    assert data == answer

    # get all submenus
    check_submenu_in_submenus(client, answer)


def test_update_submenu_and_check(db_create_menus: Session, client: TestClient):
    menu_id = '00000000-0000-0000-0000-000000000001'
    # create
    submenu_id = create_submenu(client, menu_id, random_word(12), random_word(20))

    # patch with new values
    title = random_word(13)
    description = random_word(20)
    patch_submenu(client, menu_id, submenu_id, title, description)

    answer = {
        'id': submenu_id,
        'menu_id': menu_id,
        'title': title,
        'description': description,
        'dishes_count': 0,
    }
    # get submenu by id
    check_submenu_eq_submenu(client, answer)

    # get all submenus
    check_submenu_in_submenus(client, answer)


def test_delete_submenu_and_check(db_create_menus: Session, client: TestClient):
    menu_id = '00000000-0000-0000-0000-000000000001'
    # create
    submenu_id = create_submenu(client, menu_id, random_word(14), random_word(20))

    # delete
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200

    # get submenu by id
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 404

    # check all submenus in menu
    check_submenu_not_in_submenus(client, menu_id, submenu_id)

    # check all menus
    menus = client.get('/api/v1/menus/').json()
    for menu in menus:
        check_submenu_not_in_submenus(client, menu['id'], submenu_id)


def test_delete_submenu_not_exist(db_create_menus: Session, client: TestClient):
    menu_id = '00000000-0000-0000-0000-000000000000'
    submenu_id = '00000000-0000-0000-0000-999999999999'

    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


def test_delete_submenu_menu_not_exist(db_create_menus: Session, client: TestClient):
    # create
    menu_id = '00000000-0000-0000-0000-000000000001'
    submenu_id = create_submenu(client, menu_id, random_word(14), random_word(20))
    # delete from another menu
    menu_id = '00000000-0000-0000-0000-999999999999'
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}


def test_delete_submenu_menu_and_submenu_not_exist(db_create_menus: Session, client: TestClient):
    menu_id = '00000000-0000-0000-0000-999999999999'
    submenu_id = '00000000-0000-0000-0000-999999999999'
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}
