import datetime
import logging

from db.database import DataBase
from func import convert_date
from services.data_transformation import DataTransformation
from services.excel_parsers import ExcelParser
from services.load_tables import LoadTable
from uow import UnitOfWork


logging.basicConfig(
    level=logging.INFO, format="\033[97m%(asctime)s\033[0m - \033[97m%(levelname)s\033[0m - \033[92m%(message)s\033[0m"
)

db = DataBase()
uow = UnitOfWork(db.async_session())


def async_main():
    """Главная функция запуска aсинхронного приложения."""
    start_date, end_date = convert_date()
    logging.info(f"Начало работы асинхронного приложения {datetime.datetime.now()}")
    time_now = datetime.datetime.now()
    db.async_create_db()
    loader = LoadTable(start_date, end_date)
    try:
        while True:
            table_info = loader.sync_load()
            table_date = loader.table_date
            if not table_info:
                logging.info(f"Нет данных за {table_date.strftime('%d.%m.%Y')} г.")
                continue
            parser = ExcelParser(table_info)
            table = parser.table
            transfer = DataTransformation(table, table_date)
            transfer_data_for_db = transfer.transform()
            with uow.start() as session:
                session.trading_results.add_all(transfer_data_for_db)
                logging.info(f"Загрузка информации в БД за {table_date.strftime("%d.%m.%Y")} г.")
    except StopIteration:
        logging.info("Парсинг завершен")
        logging.info(f"Время работы приложения:{datetime.datetime.now() - time_now}")  # Время работы


if __name__ == "__main__":
    async_main()
