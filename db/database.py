from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from db.config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_DRIVER


class DataBase:
    """Класс для создания базы данных"""

    DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    def __init__(self):
        self._engine = create_engine(self.__class__.DB_URL)
        self._session = sessionmaker(bind=self._engine, autoflush=False)

    @property
    def session(self):
        return self._session

    def create_db(self):
        """Создание БД"""
        # async with self._engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.drop_all)
        #     await conn.run_sync(Base.metadata.create_all)
        Base.metadata.create_all(self._engine)


class Base(DeclarativeBase):
    """Базовый класс для создания таблиц"""
    pass
