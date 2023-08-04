from typing import Generator

from sqlalchemy.engine import URL, create_engine
from sqlalchemy.orm.session import sessionmaker

from app.src.config import settings

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername='postgresql',
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    database=f'{settings.POSTGRES_DB}_test',
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator:
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()
