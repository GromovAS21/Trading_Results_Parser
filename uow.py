from contextlib import contextmanager

from repositories import TradingResultsRepository


class UnitOfWork:
    """Класс для управления транзакциями и сессиями базы данных."""

    def __init__(self, session_factory):
        """Инициализирует объект класса с заданным фабричным методом для создания сессий базы данных."""
        self.session_factory = session_factory
        self._session = None

    @contextmanager
    def start(self):
        """Контекстный менеджер для работы с базой данных."""
        self._session = self.session_factory
        try:
            yield self
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
        finally:
            self._session.close()

    @property
    def trading_results(self) -> TradingResultsRepository:
        """Создает и возвращает экземпляр TradingResultsRepository для работы в базе данных."""
        return TradingResultsRepository(self._session)
