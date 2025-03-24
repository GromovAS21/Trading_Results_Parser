from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST

DATABASE = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE)

Session = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase): pass


def create_db():
    """Создание БД при запуске сервера"""
    return Base.metadata.create_all(bind=engine)
