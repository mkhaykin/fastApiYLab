from fastapi import FastAPI

from .src.database import create_tables

from .src.routes.menu import router as menu_router
from .src.routes.submenu import router as submenu_router
from .src.routes.dishes import router as dishes_router

create_tables()

app = FastAPI()

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dishes_router)


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
