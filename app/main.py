import uvicorn
from fastapi import FastAPI

from app.src.database import create_tables
from app.src.routes.dishes import router as dishes_router
from app.src.routes.menus import router as menu_router
from app.src.routes.submenus import router as submenu_router

create_tables()

app = FastAPI()

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dishes_router)


@app.get('/')
async def hello():
    return {'msg': 'Hello World'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
