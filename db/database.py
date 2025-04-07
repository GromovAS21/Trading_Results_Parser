from sqlalchemy import create_engine, engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from abc_classes import AbstractDB
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


class Base(DeclarativeBase):
    """Базовый класс для создания таблиц."""

    pass


class SyncDataBase(AbstractDB):
    """Класс для создания синхронной базы данных."""

    DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    def __init__(self):
        """Инициализация базы данных."""
        self._engine: engine = create_engine(self.__class__.DB_URL)
        self._session: sessionmaker = sessionmaker(bind=self._engine, autoflush=False)

    @property
    def session(self) -> sessionmaker:
        """
        Возвращает синхронную сессию.

        Returns:
            sessionmaker: сессия
        """
        return self._session

    def create_db(self) -> None:
        """Создание синхронной БД."""
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)


class AsyncDataBase(AbstractDB):
    """Класс для создания aсинхронной базы данных."""

    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    def __init__(self):
        """Инициализация базы данных."""
        self._engine: engine = create_async_engine(self.__class__.DB_URL)
        self._session: async_sessionmaker = async_sessionmaker(bind=self._engine, autoflush=False)

    @property
    def session(self) -> async_sessionmaker:
        """
        Возвращает aсинхронную сессию.

        Returns:
            async_sessionmaker: сессия
        """
        return self._session

    async def create_db(self) -> None:
        """Создание асинхронной БД."""
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
