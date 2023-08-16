from functools import wraps

from fastapi import APIRouter, BackgroundTasks

from app.src.cache import Cache
from app.src.cache.handler import CacheHandler

router = APIRouter()


def cache(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        params = {
            'scope': func.__name__,
            'menu_id': kwargs.get('menu_id', None),
            'submenu_id': kwargs.get('submenu_id', None),
            'dish_id': kwargs.get('dish_id', None),
        }

        cache_handler: CacheHandler = CacheHandler(Cache())
        cached_data = await cache_handler.get(**params)
        if cached_data:
            return cached_data

        result = await func(*args, **kwargs)
        params['data'] = result

        tasks: BackgroundTasks = kwargs.get('background_tasks', None)
        if tasks:
            tasks.add_task(func=cache_handler.add, **params)
        else:
            # TODO log warning
            print('cache processing is not in the background')
            await cache_handler.add(**params)

        return result

    return wrapper


def invalidate_cache(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        params = {
            'scope': '*',
            'menu_id': kwargs.get('menu_id', None),
            'submenu_id': kwargs.get('submenu_id', None),
            'dish_id': kwargs.get('dish_id', None),
        }

        cache_handler: CacheHandler = CacheHandler(Cache())

        tasks: BackgroundTasks = kwargs.get('background_tasks', None)
        if tasks:
            tasks.add_task(func=cache_handler.delete, **params)
        else:
            # TODO log warning
            print('cache processing is not in the background')
            await cache_handler.delete(**params)

        result = await func(*args, **kwargs)
        return result

    return wrapper
