import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.test_utils import random_word
from app.tests.test_utils_menu import create_menu, menu_in_cache, patch_menu


@pytest.mark.asyncio
async def test_repeat_404(async_db: AsyncSession, async_client: AsyncClient):
    # повторяемость (не кешируем объект при его отсутствии)
    for _ in '12':
        response = await async_client.get('/api/v1/menus/99999999-0000-0000-0000-000000000000')
        assert response.status_code == 404
        assert response.json() == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_menus(async_db: AsyncSession, async_client: AsyncClient):
    title: str = random_word(11)
    description: str = random_word(20)
    menu_id: str = await create_menu(async_client, title, description)

    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200

    # TODO фикс поведение при запросе объекта другого типа
    response = await async_client.get(
        f'/api/v1/menus/{menu_id}/submenus/{menu_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_cache_menu(async_db: AsyncSession, async_client: AsyncClient):
    # проверка попадания в кэш после get
    title: str = random_word(11)
    description: str = random_word(20)
    menu_id: str = await create_menu(async_client, title, description)

    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200

    assert await menu_in_cache(menu_id)


@pytest.mark.asyncio
async def test_cache_menu_drop_after_update(async_db: AsyncSession, async_client: AsyncClient):
    # сброс кэша после обновления
    title: str = random_word(11)
    description: str = random_word(20)
    menu_id: str = await create_menu(async_client, title, description)

    # кладем в кэш
    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200

    # патчим, кэш должен быть очищен
    _ = await patch_menu(async_client, menu_id, title, description)

    assert not (await menu_in_cache(menu_id))


@pytest.mark.asyncio
async def test_cache_menu_drop_after_delete(async_db: AsyncSession, async_client: AsyncClient):
    # сброс кэша после удаления
    title: str = random_word(11)
    description: str = random_word(20)
    menu_id: str = await create_menu(async_client, title, description)

    # кладем в кэш
    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200

    # удаляем, кэш должен быть очищен
    response = await async_client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200

    assert not (await menu_in_cache(menu_id))
