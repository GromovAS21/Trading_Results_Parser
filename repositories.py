from typing import Union

from requests import Session
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import TradingResults


class TradingResultsRepository:
    """Класс для работы с таблицей TradingResults в базе данных."""

    def __init__(self, session: Union[Session, AsyncSession]):
        """
        Инициализация репозитория.

        Args:
            session (Session, AsyncSession): Объект сессии для работы с базой данных.
        """
        self._session: Union[Session, AsyncSession] = session

    def add_all(self, results: list[TradingResults]):
        """
        Добавить все записи в базу данных.

        Args:
            results (list[TradingResults]): Список записей для добавления.
        """
        self._session.add_all(results)
