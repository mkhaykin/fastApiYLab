from uuid import UUID

import xlrd

from app.src import schemas
from app.src.repos import DishesRepository, MenuRepository, SubMenuRepository

from .base import BaseService


class XlsItem:
    def __init__(self):
        self.menu_id: str = ''
        self.menu: str = ''
        self.menu_desc: str = ''
        self.submenu_id: str = ''
        self.submenu: str = ''
        self.submenu_desc: str = ''
        self.dish_id: str = ''
        self.dish: str = ''
        self.dish_desc: str = ''
        self.dish_price: str = ''
        self.dish_discount: str = ''

    def __str__(self):
        return str(self.__dict__)


def silent(func):
    async def wrapped(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except Exception as e:
            # TODO write log
            print(f'error: {str(e)}')

    return wrapped


@silent
async def _read_file(filename: str) -> list[XlsItem]:
    wb = xlrd.open_workbook(filename)
    ws = wb.sheet_by_index(0)
    data: list[XlsItem] = []
    for row in range(0, ws.nrows):
        item = XlsItem()
        if ws.cell(row, 0).value:
            item.menu_id = ws.cell(row, 0).value
            item.menu = ws.cell(row, 1).value
            item.menu_desc = ws.cell(row, 3).value
        else:
            item.menu_id = data[-1].menu_id
            item.menu = data[-1].menu
            item.menu_desc = data[-1].menu_desc
            if ws.cell(row, 1).value:
                item.submenu_id = ws.cell(row, 1).value
                item.submenu = ws.cell(row, 2).value
                item.submenu_desc = ws.cell(row, 3).value
            else:
                item.submenu_id = data[-1].submenu_id
                item.submenu = data[-1].submenu
                item.submenu_desc = data[-1].submenu_desc
                item.dish_id = ws.cell(row, 2).value
                item.dish = ws.cell(row, 3).value
                item.dish_desc = ws.cell(row, 4).value
                item.dish_price = ws.cell(row, 5).value
                item.dish_discount = ws.cell(row, 6).value

        data.append(item)
    return data


class XlsMenuService(BaseService):
    def __init__(self,
                 # repo_menus: MenuRepository = Depends(),
                 # repo_submenus: SubMenuRepository = Depends(),
                 # repo_dishes: DishesRepository = Depends(),
                 db, cache
                 ):
        # self.repo_menus = repo_menus
        # self.repo_submenus = repo_submenus
        # self.repo_dishes = repo_dishes
        self.repo_menus = MenuRepository(db, cache)
        self.repo_submenus = SubMenuRepository(db, cache)
        self.repo_dishes = DishesRepository(db, cache)

    async def load_from_file(self, filename: str) -> None:
        # читаем файл в list
        data: list[XlsItem] = await _read_file(filename)

        if not data:
            # TODO write log
            print('ошибка чтения файла')
            return

        # делаем сет-ы уникальных объектов (чтобы быстро удалить не существующие пункты)
        menus_ids = set()
        submenus_ids = set()
        dishes_ids = set()
        for item in data:
            menus_ids.add(item.menu_id)
            submenus_ids.add(item.submenu_id)
            dishes_ids.add(item.dish_id)

        # проходим по каждому объекту
        for item in data:
            if item.dish_id:
                await self._patch_dish(
                    item.menu_id,
                    item.submenu_id, item.dish_id, item.dish, item.dish_desc,
                    item.dish_price, item.dish_discount)
            elif item.submenu_id:
                await self._patch_submenu(item.menu_id, item.submenu_id, item.submenu, item.submenu_desc)
            elif item.menu_id:
                await self._patch_menu(item.menu_id, item.menu, item.menu_desc)
            else:
                pass  # пропуск пустой строки если есть

        # удаляем не существующие пункты
        await self._clear_menu_except(menus_ids, submenus_ids, dishes_ids)
        pass

    @silent
    async def _patch_menu(self, menu_id, menu, menu_desc):
        if await self.repo_menus.get_by_ids(menu_id):
            await self.repo_menus.update_menu(
                menu_id,
                schemas.UpdateMenuIn(
                    title=menu,
                    description=menu_desc
                ),
            )
        else:
            await self.repo_menus.create_menu(
                schemas.CreateMenuIn(
                    title=menu,
                    description=menu_desc
                ),
                obj_id=menu_id
            )

    @silent
    async def _patch_submenu(self, menu_id, submenu_id, submenu, submenu_desc):
        if await self.repo_submenus.get_by_ids(menu_id, submenu_id):
            await self.repo_submenus.update_submenu(
                menu_id,
                submenu_id,
                schemas.UpdateSubMenuIn(
                    title=submenu,
                    description=submenu_desc
                ),
            )
        else:
            await self.repo_submenus.create_submenu(
                menu_id,
                schemas.CreateSubMenuIn(
                    title=submenu,
                    description=submenu_desc
                ),
                obj_id=submenu_id,
            )

    @silent
    async def _patch_dish(self, menu_id, submenu_id, dish_id, dish, dish_desc, dish_price, dish_discount):
        # TODO dish_discount
        if await self.repo_dishes.get_by_ids(menu_id, submenu_id, dish_id):
            await self.repo_dishes.update_dish(
                menu_id,
                submenu_id,
                dish_id,
                schemas.UpdateDishIn(title=dish,
                                     description=dish_desc,
                                     price=dish_price,
                                     ),
            )
        else:
            await self.repo_dishes.create_dish(
                menu_id,
                submenu_id,
                schemas.CreateDishIn(
                    title=dish,
                    description=dish_desc,
                    price=dish_price,
                ),
                obj_id=dish_id,
            )

    @silent
    async def _clear_menu_except(
            self,
            existing_menus: set,
            existing_submenus: set,
            existing_dishes: set
    ):
        menus: list[schemas.GetMenu] = await self.repo_menus.get_by_ids()
        for menu in menus:
            if str(menu.id) not in existing_menus:
                await self.repo_menus.delete_menu(menu.id)
            else:
                await self._clear_submenu_except(menu.id, existing_submenus, existing_dishes)

    @silent
    async def _clear_submenu_except(
            self,
            menu_id: UUID,
            existing_submenus: set,
            existing_dishes: set
    ):
        submenus: list[schemas.GetSubMenu] = await self.repo_submenus.get_by_ids(menu_id=menu_id)
        for submenu in submenus:
            if str(submenu.id) not in existing_submenus:
                await self.repo_submenus.delete_submenu(menu_id, submenu.id)
            else:
                await self._clear_dishes_except(menu_id, submenu.id, existing_dishes)

    @silent
    async def _clear_dishes_except(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            existing_dishes: set
    ):
        dishes: list[schemas.GetDish] = await self.repo_dishes.get_by_ids(menu_id=menu_id, submenu_id=submenu_id)
        for dish in dishes:
            if str(dish.id) not in existing_dishes:
                await self.repo_dishes.delete_dish(menu_id, submenu_id, dish.id)
