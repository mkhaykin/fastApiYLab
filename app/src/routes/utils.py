from functools import wraps

from fastapi import APIRouter, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

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
        background_task: BackgroundTasks = BackgroundTasks()
        if background_task:
            background_task.add_task(func=cache_handler.add, **params)
        else:
            # TODO log warning
            print('cache processing is not in the background')
            await cache_handler.add(**params)
        return JSONResponse(jsonable_encoder(result), background=background_task)

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
        background_task: BackgroundTasks = BackgroundTasks()
        if background_task:
            background_task.add_task(func=cache_handler.delete, **params)
        else:
            # TODO log warning
            print('cache processing is not in the background')
            await cache_handler.delete(**params)

        result = await func(*args, **kwargs)
        return JSONResponse(jsonable_encoder(result), background=background_task)

    return wrapper
