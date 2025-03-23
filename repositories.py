from database import Session
from models import TradingResults


class TradingResultsRepository:

    def __init__(self, session: Session):
        self._session = session

    def add_all(self, results: list[TradingResults]):
        return self._session.add_all(results)
