from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings


SQLALCHEMY_DATABASE_URL = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    settings.POSTGRES_USER,
    settings.POSTGRES_PASSWORD,
    settings.POSTGRES_HOST,
    settings.DATABASE_PORT,
    settings.POSTGRES_DB,
)

print("!!!!")
print(SQLALCHEMY_DATABASE_URL)
print("!!!!")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(engine)
Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
