from uuid import UUID

from app.tests.database import TestingSession
from app.tests.utils import random_word
from app.tests.utils_menu import (
    check_menu_eq_menu,
    check_menu_in_menus,
    check_menu_not_in_menus,
    create_menu,
    patch_menu,
)


def test_menus(db_test: TestingSession, client):
    response = client.get('/api/v1/menus')
    assert response.status_code == 200
    # assert not response.json()    # data must be cleared for this test


def test_menu_not_found(db_test, client):
    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}


def test_create_menu_fix(db_test, client):
    create_menu(client, 'My menu 1', 'My menu description 1')


def test_create_menu_duplicate(db_test, client):
    title, description = 'My menu 2', 'My menu description 2'
    create_menu(client, title, description)
    response = client.post(
        '/api/v1/menus',
        json={'title': title, 'description': description},
    )
    assert response.status_code == 409


def test_create_menu_random(db_test, client):
    title = random_word(10)
    description = random_word(20)
    create_menu(client, title, description)


def test_create_menu_and_find_it(db_test, client):
    # create
    title: str = random_word(11)
    description: str = random_word(20)
    menu_id: UUID = create_menu(client, title, description)

    # check
    answer = {
        'id': menu_id,
        'title': title,
        'description': description,
        'submenus_count': 0,
        'dishes_count': 0,
    }
    check_menu_eq_menu(client, answer)


def test_create_menu_and_find_it_in_menus(db_test, client):
    # create
    title = random_word(12)
    description = random_word(20)
    menu_id = create_menu(client, title, description)

    # check
    answer = {
        'id': menu_id,
        'title': title,
        'description': description,
        'submenus_count': 0,
        'dishes_count': 0,
    }
    check_menu_in_menus(client, answer)


def test_update_menu_and_find_it(db_test, client):
    # create menu
    menu_id = create_menu(client, random_word(13), random_word(20))
    # patch with new values
    title = random_word(14)
    description = random_word(20)
    patch_menu(client, menu_id, title, description)

    # check
    answer = {
        'id': menu_id,
        'title': title,
        'description': description,
        'submenus_count': 0,
        'dishes_count': 0,
    }
    check_menu_eq_menu(client, answer)


def test_update_menu_and_find_it_in_menus(db_test, client):
    menu_id = create_menu(client, random_word(15), random_word(20))
    # patch with new values
    title = random_word(16)
    description = random_word(20)
    patch_menu(client, menu_id, title, description)

    # check
    answer = {
        'id': menu_id,
        'title': title,
        'description': description,
        'submenus_count': 0,
        'dishes_count': 0,
    }
    check_menu_eq_menu(client, answer)


def test_delete_menu(db_test, client):
    menu_id = create_menu(client, random_word(17), random_word(20))
    response = client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200


def test_delete_menu_not_exist(db_test, client):
    menu_id = '00000000-0000-0000-0000-000000000000'
    response = client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 404


def test_delete_menu_and_check(db_test, client):
    # create
    menu_id = create_menu(client, random_word(18), random_word(20))
    # delete
    response = client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    # check by menu_id
    response = client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}
    # check in menus
    check_menu_not_in_menus(client, menu_id)
