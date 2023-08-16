import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.tests.utils import random_word

from .utils_cache import cache_reset
from .utils_menu import (
    create_menu,
    delete_menu,
    get_menu,
    get_menus,
    menu_in_cache,
    menus_in_cache,
    patch_menu,
)


@pytest_asyncio.fixture(scope='function')
async def create_menu_and_cache(async_client):
    await cache_reset()
    title = random_word(10)
    description = random_word(20)
    menu_id: str = await create_menu(async_client, title, description)
    _ = await get_menus(async_client)
    _ = await get_menu(async_client, menu_id)

    yield menu_id
    # await delete_menu(async_client, menu_id)


@pytest.mark.asyncio
async def test_menu_in_cache_after_get(create_menu_and_cache: str, async_client: AsyncClient):
    menu_id = create_menu_and_cache
    assert await menu_in_cache(menu_id)


@pytest.mark.asyncio
async def test_menu_not_in_cache_after_patch(create_menu_and_cache: str, async_client: AsyncClient):
    menu_id = create_menu_and_cache
    await patch_menu(async_client, menu_id, random_word(11), random_word(12))
    assert not (await menu_in_cache(menu_id))


@pytest.mark.asyncio
async def test_menu_not_in_cache_after_delete(create_menu_and_cache: str, async_client: AsyncClient):
    menu_id = create_menu_and_cache
    await delete_menu(async_client, menu_id)
    assert not (await menu_in_cache(menu_id))


@pytest.mark.asyncio
async def test_menu_not_in_cache_after_create(create_menu_and_cache: str, async_client: AsyncClient):
    menu_id = create_menu_and_cache
    menu_id2: str = await create_menu(async_client, random_word(12), random_word(12))
    assert (await menu_in_cache(menu_id))
    assert not (await menus_in_cache())
    assert not (await menu_in_cache(menu_id2))
