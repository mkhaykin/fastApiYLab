import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.test_data import MENU_ID_WRONG
from app.tests.test_utils import random_word
from app.tests.test_utils_menu import (
    create_menu,
    delete_menu,
    get_menu,
    menu_in_cache,
    patch_menu,
)
from app.tests.test_utils_submenu import get_submenu


@pytest.mark.asyncio
async def test_repeat_404(async_db: AsyncSession, async_client: AsyncClient):
    # повторяемость (не кешируем объект при его отсутствии)
    for _ in '12':
        data = await get_menu(async_client, MENU_ID_WRONG, waited_code=404)
        assert data == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_menus(async_db: AsyncSession, async_client: AsyncClient):
    menu_id: str = await create_menu(async_client, random_word(11), random_word(20))

    # получаем и кешируем
    await get_menu(async_client, menu_id)

    # при запросе другого объекта с подходящим id не должны получить кэш
    data = await get_submenu(async_client, menu_id, menu_id, waited_code=404)
    assert data == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_cache_menu(async_db: AsyncSession, async_client: AsyncClient):
    # проверка попадания в кэш после get
    menu_id: str = await create_menu(async_client, random_word(11), random_word(20))
    # кладем в кэш
    await get_menu(async_client, menu_id)
    # проверяем в кеше
    assert await menu_in_cache(menu_id)


@pytest.mark.asyncio
async def test_cache_menu_drop_after_update(async_db: AsyncSession, async_client: AsyncClient):
    # сброс кэша после обновления
    menu_id: str = await create_menu(async_client, random_word(11), random_word(20))

    # кладем в кэш
    await get_menu(async_client, menu_id)
    # патчим, кэш должен быть очищен
    _ = await patch_menu(async_client, menu_id, random_word(11), random_word(20))

    assert not (await menu_in_cache(menu_id))


@pytest.mark.asyncio
async def test_cache_menu_drop_after_delete(async_db: AsyncSession, async_client: AsyncClient):
    # сброс кэша после удаления
    menu_id: str = await create_menu(async_client, random_word(11), random_word(20))

    # кладем в кэш
    await get_menu(async_client, menu_id)

    # удаляем, кэш должен быть очищен
    await delete_menu(async_client, menu_id)

    assert not (await menu_in_cache(menu_id))
