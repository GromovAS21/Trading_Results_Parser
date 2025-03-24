from database import Session
from models import TradingResults


class TradingResultsRepository:
    """Класс для работы с таблицей TradingResults в базе данных"""

    def __init__(self, session: Session):
        self._session = session

    def add_all(self, results: list[TradingResults]):
        return self._session.add_all(results)
