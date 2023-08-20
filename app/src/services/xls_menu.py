from uuid import UUID

from fastapi import Depends

from app.src import schemas
from app.src.repos import DishesRepository, MenuRepository, SubMenuRepository
from app.src.services.xls_menu_loader import (
    LoaderStatus,
    TXlsLoader,
    XlsFileLoader,
    XlsSheetLoader,
)

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


class ErrorCount:
    """
    Счетчик ошибок декоратора
    """

    def __init__(self):
        self._count = 0

    @property
    def count(self):
        return self._count

    def inc(self):
        self._count += 1

    def reset(self):
        self._count = 0

    def __str__(self):
        return super().__str__() + ' Values: ' + str(self._count)


class XlsMenuService(BaseService):
    def __init__(self,
                 repo_menus: MenuRepository = Depends(),
                 repo_submenus: SubMenuRepository = Depends(),
                 repo_dishes: DishesRepository = Depends(),
                 ):
        self.repo_menus = repo_menus
        self.repo_submenus = repo_submenus
        self.repo_dishes = repo_dishes

        self.error_counter = ErrorCount()

    @staticmethod
    def silent(func):
        async def wrapped(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except Exception as e:
                if self.error_counter:
                    self.error_counter.inc()
                # TODO write log
                print(f'error: {str(e)}')

        return wrapped

    @staticmethod
    def parse_row(row: list, prev_item: XlsItem) -> XlsItem:
        item = XlsItem()
        if row[0]:
            item.menu_id = row[0]
            item.menu = row[1]
            item.menu_desc = row[2]
        else:
            item.menu_id = prev_item.menu_id
            item.menu = prev_item.menu
            item.menu_desc = prev_item.menu_desc
            if row[1]:
                item.submenu_id = row[1]
                item.submenu = row[2]
                item.submenu_desc = row[3]
            else:
                item.submenu_id = prev_item.submenu_id
                item.submenu = prev_item.submenu
                item.submenu_desc = prev_item.submenu_desc
                item.dish_id = row[2]
                item.dish = row[3]
                item.dish_desc = row[4]
                item.dish_price = row[5]
                item.dish_discount = row[6]
        return item

    async def _load_data(self, data: list[XlsItem]):
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
                    item.dish_price, item.dish_discount,
                )
            elif item.submenu_id:
                await self._patch_submenu(item.menu_id, item.submenu_id, item.submenu, item.submenu_desc)
            elif item.menu_id:
                await self._patch_menu(item.menu_id, item.menu, item.menu_desc)
            else:
                pass  # пропуск пустой строки если есть

        # удаляем не существующие пункты
        await self._clear_menu_except(menus_ids, submenus_ids, dishes_ids)

    async def _load(self, loader: TXlsLoader) -> schemas.MessageMenuLoad:
        loader.load()
        msg = schemas.MessageMenuLoad()
        msg.detail = loader.message

        self.error_counter.reset()
        if loader.status == LoaderStatus.loaded:
            data: list[XlsItem] = [XlsItem()]
            for row in loader:
                item = self.parse_row(row, data[-1])
                data.append(item)
            await self._load_data(data[1:])
        if self.error_counter.count:
            msg.error_count = self.error_counter.count
        return msg

    async def load_from_file(self, filename: str) -> schemas.MessageMenuLoad:
        return await self._load(XlsFileLoader(filename))

    async def load_from_sheet(self, source: str) -> schemas.MessageMenuLoad:
        return await self._load(XlsSheetLoader(source))

    @silent
    async def _patch_menu(self, menu_id, menu, menu_desc):
        if await self.repo_menus.get_by_ids(menu_id):
            await self.repo_menus.update_menu(
                menu_id,
                schemas.UpdateMenuIn(
                    title=menu,
                    description=menu_desc,
                ),
            )
        else:
            await self.repo_menus.create_menu(
                schemas.CreateMenuIn(
                    title=menu,
                    description=menu_desc,
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
                    description=submenu_desc,
                ),
            )
        else:
            await self.repo_submenus.create_submenu(
                menu_id,
                schemas.CreateSubMenuIn(
                    title=submenu,
                    description=submenu_desc,
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
                schemas.UpdateDishIn(
                    title=dish,
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
            existing_dishes: set,
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
            existing_dishes: set,
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
            existing_dishes: set,
    ):
        dishes: list[schemas.GetDish] = await self.repo_dishes.get_by_ids(menu_id=menu_id, submenu_id=submenu_id)
        for dish in dishes:
            if str(dish.id) not in existing_dishes:
                await self.repo_dishes.delete_dish(menu_id, submenu_id, dish.id)
