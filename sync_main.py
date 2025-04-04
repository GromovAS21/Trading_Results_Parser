import datetime
import logging

from db.database import DataBase
from services.data_transformation import DataTransformation
from services.excel_parsers import ExcelParser
from services.load_tables import LoadTable
from uow import UnitOfWork


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


db = DataBase()
uow = UnitOfWork(db.sync_session())


def sync_main():
    """Главная функция запуска синхронного приложения."""
    start_date, end_date = (datetime.datetime(2023, 1, 1), datetime.datetime(2025, 4, 4))
    logging.info(f"Начало работы приложения {datetime.datetime.now()}")
    time_now = datetime.datetime.now()
    db.sync_create_db()
    loader = LoadTable(start_date, end_date)
    try:
        while True:
            table_info = loader.sync_load()
            if table_info:
                table_date = loader.table_date
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
    sync_main()
