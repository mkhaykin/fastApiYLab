"""
    на момент теста у нас 2 записи по меню, 3 записи submenu и 3 записи dish
    00000000-0000-0000-0000-000000000000
        00000000-0000-0000-0000-000000000000
            00000000-0000-0000-0000-000000000000
            00000000-0000-0000-0000-000000000001
        00000000-0000-0000-0000-000000000001
            00000000-0000-0000-0000-000000000002
    00000000-0000-0000-0000-000000000001
        00000000-0000-0000-0000-000000000002
"""
from app.tests.utils import random_word


def test_menu_exist(db_create_dishes, client):
    response = client.get('/api/v1/menus/')
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 200

    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000001')
    assert response.status_code == 200


def test_submenu_exist(db_create_dishes, client):
    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000/submenus')
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000001/submenus')
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get(
        '/api/v1/menus/00000000-0000-0000-0000-000000000000/'
        'submenus/00000000-0000-0000-0000-000000000000'
    )
    assert response.status_code == 200
    response = client.get(
        '/api/v1/menus/00000000-0000-0000-0000-000000000000/'
        'submenus/00000000-0000-0000-0000-000000000001'
    )
    assert response.status_code == 200
    response = client.get(
        '/api/v1/menus/00000000-0000-0000-0000-000000000001/'
        'submenus/00000000-0000-0000-0000-000000000002'
    )
    assert response.status_code == 200


def test_dishes_exist(db_create_dishes, client):
    response = client.get(
        '/api/v1/menus/00000000-0000-0000-0000-000000000000/'
        'submenus/00000000-0000-0000-0000-000000000000/'
        'dishes'
    )
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.get(
        '/api/v1/menus/00000000-0000-0000-0000-000000000000/'
        'submenus/00000000-0000-0000-0000-000000000001/'
        'dishes'
    )
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get(
        '/api/v1/menus/00000000-0000-0000-0000-000000000001/'
        'submenus/00000000-0000-0000-0000-000000000002/'
        'dishes'
    )
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = client.get(
        '/api/v1/menus/00000000-0000-0000-0000-000000000000/'
        'submenus/00000000-0000-0000-0000-000000000000/'
        'dishes/00000000-0000-0000-0000-000000000000/'
    )
    assert response.status_code == 200

    response = client.get(
        '/api/v1/menus/00000000-0000-0000-0000-000000000000/'
        'submenus/00000000-0000-0000-0000-000000000000/'
        'dishes/00000000-0000-0000-0000-000000000001/'
    )
    assert response.status_code == 200

    response = client.get(
        '/api/v1/menus/00000000-0000-0000-0000-000000000000/'
        'submenus/00000000-0000-0000-0000-000000000001/'
        'dishes/00000000-0000-0000-0000-000000000002/'
    )
    assert response.status_code == 200


def test_start_counts(db_create_dishes, client):
    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 2
    assert response.json()['dishes_count'] == 3

    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000001')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 1
    assert response.json()['dishes_count'] == 0


def test_submenus_count(db_create_dishes, client):
    menu_id = '00000000-0000-0000-0000-000000000000'
    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 200
    submenus_count = response.json()['submenus_count']
    dishes_count = response.json()['dishes_count']
    # create submenu
    response = client.post(
        f'/api/v1/menus/{menu_id}/submenus',
        json={
            'title': f'{random_word(10)}',
            'description': f'{random_word(20)}',
        },
    )
    assert response.status_code == 201
    submenu_id = response.json()['id']
    # check count: submenu + 1
    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == submenus_count + 1
    assert response.json()['dishes_count'] == dishes_count
    # delete submenu
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    # check count: submenu back to start value
    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == submenus_count
    assert response.json()['dishes_count'] == dishes_count


def test_dishes_count(db_create_dishes, client):
    menu_id = '00000000-0000-0000-0000-000000000000'
    submenu_id = '00000000-0000-0000-0000-000000000000'
    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 200
    submenus_count = response.json()['submenus_count']
    dishes_count = response.json()['dishes_count']
    # create dish
    response = client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json={
            'title': f'{random_word(10)}',
            'description': f'{random_word(20)}',
            'price': '1',
        },
    )
    assert response.status_code == 201
    dish_id = response.json()['id']
    # check count: submenu + 1
    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == submenus_count
    assert response.json()['dishes_count'] == dishes_count + 1
    # delete dish
    response = client.delete(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    assert response.status_code == 200
    # check count: submenu start value
    response = client.get('/api/v1/menus/00000000-0000-0000-0000-000000000000')
    assert response.status_code == 200
    assert response.json()['submenus_count'] == submenus_count
    assert response.json()['dishes_count'] == dishes_count
