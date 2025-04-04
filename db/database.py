from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from db.config import DB_DRIVER, DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


class DataBase:
    """Класс для создания базы данных."""

    DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    def __init__(self):
        """Инициализация базы данных."""
        self._engine = create_engine(self.__class__.DB_URL)
        self._session = sessionmaker(bind=self._engine, autoflush=False)

    @property
    def session(self):
        """
        Возвращает сессию.

        Returns:
            sessionmaker: сессия
        """
        return self._session

    def create_db(self):
        """Создание БД."""
        Base.metadata.create_all(self._engine)


class Base(DeclarativeBase):
    """Базовый класс для создания таблиц."""

    pass
