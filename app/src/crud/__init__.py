from .menus import crud_menus
from .submenus import crud_submenus
from .dishes import crud_dishes

__all__ = [crud_menus, crud_submenus, crud_dishes]

# from .menu import menu_get_all, menu_get, menu_create, menu_update, menu_delete, crud_menus
#
# __all__ = ["menu_get_all", "menu_get", "menu_create", "menu_update", "menu_update", crud_menus]
# from .menus import Menus, UpdateMenu, CreateMenu
# from .submenus import SubMenus, UpdateSubMenu
# from .dishes import Dishes, UpdateDish
#
# __all__ = ["Menus", "UpdateMenu", "CreateMenu", "SubMenus", "UpdateSubMenu", "Dishes", "UpdateDish"]
