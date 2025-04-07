from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker


class AbstractDB(ABC):
    """Абстрактный класс для работы с БД."""

    @abstractmethod
    def session(self) -> Union[sessionmaker, async_sessionmaker]:
        """Возвращает сессию."""
        pass

    @abstractmethod
    def create_db(self) -> None:
        """Создает структуру БД."""
        pass


class AbstractLoader(ABC):
    """Абстрактный класс для загрузки таблиц."""

    @abstractmethod
    def _path_file(self) -> Path:
        """Возвращает путь к файлу с данными."""
        pass

    @abstractmethod
    def _get_filename(self) -> str:
        """Возвращает имя файла."""
        pass

    @abstractmethod
    def load(self) -> bytes:
        """Загружает данные по url адресу."""
        pass
