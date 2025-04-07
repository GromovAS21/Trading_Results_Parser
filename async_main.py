import asyncio
import datetime
import logging

from config import MAX_CONCURRENT_TASKS
from db.database import AsyncDataBase
from func import convert_date, gen_date
from services.date_transform import DataTransformer
from services.loaders import AsyncLoader
from services.parsers import ExcelParser
from uow import UnitOfWork


logging.basicConfig(
    level=logging.INFO, format="\033[97m%(asctime)s\033[0m - \033[97m%(levelname)s\033[0m - \033[92m%(message)s\033[0m"
)

db = AsyncDataBase()
semaphore = asyncio.Semaphore(int(MAX_CONCURRENT_TASKS))  # Ограничение на количество одновременных запросов


async def process_single_date(loader: AsyncLoader, date: datetime.date) -> None:
    """
    Обрабатывает одну дату и сохраняет в БД.

    Args:
        loader (AsyncLoader): Объект для загрузки данных из файла.
        date (datetime.datetime): Дата для обработки.
    """
    async with semaphore:
        uow = UnitOfWork(db.session())
        table_info = await loader.load()
        if not table_info:
            logging.info(f"Нет данных за {date.strftime('%d.%m.%Y')} г.")
            return  # Если нет данных, пропускаем эту дату

        parser = ExcelParser(table_info)
        table = parser.table
        transfer = DataTransformer(table, date)
        transfer_data_for_db = transfer.transform()

        async with uow.async_start() as session:
            session.trading_results.add_all(transfer_data_for_db)
            logging.info(f"Загрузка информации в БД за {date.strftime("%d.%m.%Y")} г.")


async def async_main() -> None:
    """Главная функция запуска aсинхронного приложения."""
    start_date, end_date = convert_date()
    date_generator = gen_date(start_date)
    logging.info(f"Начало работы асинхронного приложения {datetime.datetime.now()}")
    time_now = datetime.datetime.now()
    await db.create_db()

    tasks = []

    while True:
        date = next(date_generator)  # Получаем следующую дату
        if date > end_date:  # Проверяем, не достигли ли мы конечной даты
            break

        try:
            loader = AsyncLoader(date)
            task = asyncio.create_task(process_single_date(loader, date))
            tasks.append(task)
        except TimeoutError:
            logging.error(f"Превышено время ожидания загрузки данных за {date.strftime('%d.%m.%Y')} г.")

    await asyncio.gather(*tasks)

    logging.info("Парсинг завершен")
    logging.info(f"Время работы приложения:{datetime.datetime.now() - time_now}")


if __name__ == "__main__":
    asyncio.run(async_main())
