from db.models import TradingResults


class TradingResultsRepository:
    """Класс для работы с таблицей TradingResults в базе данных"""

    def __init__(self, session):
        """
        Инициализация репозитория.

        Args:
            session (Session): Объект сессии для работы с базой данных.
        """
        self._session = session

    def add_all(self, results: list[TradingResults]):
        """
        Добавить все записи в базу данных.

        Args:
            results (list[TradingResults]): Список записей для добавления.
        """
        self._session.add_all(results)
