from sqlalchemy.engine import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from app.src.config import settings


SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    database=settings.POSTGRES_DB,
)


class Base(DeclarativeBase):
    pass


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
Session = sessionmaker(engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)


def drop_tables():
    Base.metadata.drop_all(bind=engine)
