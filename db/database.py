from sqlalchemy import create_engine, engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from db.config import DB_DRIVER, DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


class DataBase:
    """Класс для создания базы данных."""

    DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    def __init__(self):
        """Инициализация базы данных."""
        self._engine: engine = create_engine(self.__class__.DB_URL)
        self._sync_session: sessionmaker = sessionmaker(bind=self._engine, autoflush=False)

    @property
    def sync_session(self):
        """
        Возвращает синхронную сессию.

        Returns:
            sessionmaker: сессия
        """
        return self._sync_session

    def sync_create_db(self):
        """Создание Синхронное БД."""
        Base.metadata.create_all(self._engine)


class Base(DeclarativeBase):
    """Базовый класс для создания таблиц."""

    pass
