from typing import AsyncGenerator

from sqlalchemy.engine import URL, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.src.config import settings

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername='postgresql',
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    database=settings.POSTGRES_DB,
)

SQLALCHEMY_DATABASE_URL_async = URL.create(
    drivername='postgresql+asyncpg',
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    database=settings.POSTGRES_DB,
)


class Base(DeclarativeBase):
    pass


# engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
# engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True,)
# Session = sessionmaker(engine)
# Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # echo=settings.db_echo_log,
)

engine_async = create_async_engine(
    SQLALCHEMY_DATABASE_URL_async,
    # echo=settings.db_echo_log,
    future=True,
)


async_session = sessionmaker(
    bind=engine_async, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        # async with session.begin():
        yield session


async def async_create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def async_drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SYNC
# Session = sessionmaker(engine)

# def get_db():
#     db = Session()
#     try:
#         yield db
#     finally:
#         db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)


def drop_tables():
    Base.metadata.drop_all(bind=engine)
