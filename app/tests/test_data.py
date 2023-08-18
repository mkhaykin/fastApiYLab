MENU_ID1 = '00000000-0001-0000-0000-000000000000'
MENU_ID2 = '00000000-0002-0000-0000-000000000000'
MENU_ID_WRONG = '00000000-9999-0000-0000-000000000000'

SUBMENU_ID11 = '00000000-0000-0001-0000-000000000000'
SUBMENU_ID12 = '00000000-0000-0002-0000-000000000000'
SUBMENU_ID23 = '00000000-0000-0003-0000-000000000000'
SUBMENU_ID_WRONG = '00000000-0000-9999-0000-000000000000'

DISH_ID111 = '00000000-0000-0000-0001-000000000000'
DISH_ID112 = '00000000-0000-0000-0002-000000000000'
DISH_ID123 = '00000000-0000-0000-0003-000000000000'
DISH_ID_WRONG = '00000000-0000-0000-9999-000000000000'

MENU1 = {
    'id': MENU_ID1,
    'title': 'Menu 1 title',
    'description': 'Menu 1 description',
}

MENU2 = {
    'id': MENU_ID2,
    'title': 'Menu 2 title',
    'description': 'Menu 2 description',
}

SUBMENU1 = {
    'id': SUBMENU_ID11,
    'menu_id': MENU_ID1,
    'title': 'SubMenu 1 title',
    'description': 'SubMenu 11 description',
}

SUBMENU2 = {
    'id': SUBMENU_ID12,
    'menu_id': MENU_ID1,
    'title': 'SubMenu 2 title',
    'description': 'SubMenu 12 description',
}

SUBMENU3 = {
    'id': SUBMENU_ID23,
    'menu_id': MENU_ID2,
    'title': 'SubMenu 3 title',
    'description': 'SubMenu 21 description',
}

DISH1 = {
    'id': DISH_ID111,
    'submenu_id': SUBMENU_ID11,
    'title': 'Dish 1 title',
    'description': 'Dish 1 description',
    'price': '9.99',
}

DISH2 = {
    'id': DISH_ID112,
    'submenu_id': SUBMENU_ID11,
    'title': 'Dish 2 title',
    'description': 'Dish 2 description',
    'price': '10.10',
}

DISH3 = {
    'id': DISH_ID123,
    'submenu_id': SUBMENU_ID12,
    'title': 'Dish 3 title',
    'description': 'Dish 3 description',
    'price': '11.11',
}
