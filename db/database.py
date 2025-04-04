from sqlalchemy import create_engine, engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from db.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


class DataBase:
    """Класс для создания базы данных."""

    SYNC_DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    ASYNC_DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    def __init__(self):
        """Инициализация базы данных."""
        self._engine: engine = create_engine(self.__class__.SYNC_DB_URL)
        self._async_engine: engine = create_async_engine(self.__class__.ASYNC_DB_URL)
        self._sync_session: sessionmaker = sessionmaker(bind=self._engine, autoflush=False)
        self._async_session: async_sessionmaker = async_sessionmaker(bind=self._async_engine, autoflush=False)

    @property
    def sync_session(self):
        """
        Возвращает синхронную сессию.

        Returns:
            sessionmaker: сессия
        """
        return self._sync_session

    @property
    def async_session(self):
        """
        Возвращает aсинхронную сессию.

        Returns:
            async_sessionmaker: сессия
        """
        return self._async_session

    def sync_create_db(self):
        """Создание синхронной БД."""
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

    async def async_create_db(self):
        """Создание асинхронной БД."""
        with self._async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


class Base(DeclarativeBase):
    """Базовый класс для создания таблиц."""

    pass
