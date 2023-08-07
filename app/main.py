import asyncio

import uvicorn
from fastapi import FastAPI

from app.src.cache.actions import cache_reset
from app.src.database import create_tables
from app.src.routes.dishes import router as dishes_router
from app.src.routes.menus import router as menu_router
from app.src.routes.submenus import router as submenu_router

create_tables()

app = FastAPI()

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dishes_router)


async def main():
    await cache_reset()
    uvicorn.run(app, host='0.0.0.0', port=8000)


@app.get('/')
async def read_main():
    return {'msg': 'Hello World'}


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
