from contextlib import asynccontextmanager, contextmanager
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from repositories import TradingResultsRepository


class UnitOfWork:
    """Класс для управления транзакциями и сессиями базы данных."""

    def __init__(self, session: Union[Session, AsyncSession]):
        """Инициализирует объект класса с заданным фабричным методом для создания сессий базы данных."""
        self._session = session

    @contextmanager
    def sync_start(self):
        """Синхронный контекстный менеджер для работы с базой данных."""
        try:
            yield self
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
        finally:
            self._session.close()

    @asynccontextmanager
    async def async_start(self):
        """Асинхронный контекстный менеджер для работы с базой данных."""
        try:
            yield self
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e
        finally:
            await self._session.close()

    @property
    def trading_results(self) -> TradingResultsRepository:
        """Создает и возвращает экземпляр TradingResultsRepository для работы в базе данных."""
        return TradingResultsRepository(self._session)
