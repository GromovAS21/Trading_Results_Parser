import datetime
import logging

from db.database import SyncDataBase
from func import convert_date, gen_date
from services.date_transform import DataTransformer
from services.loaders import SyncLoader
from services.parsers import ExcelParser
from uow import UnitOfWork


logging.basicConfig(
    level=logging.INFO, format="\033[97m%(asctime)s\033[0m - \033[97m%(levelname)s\033[0m - \033[92m%(message)s\033[0m"
)

db = SyncDataBase()
uow = UnitOfWork(db.session())


def sync_main() -> None:
    """Главная функция запуска синхронного приложения."""
    start_date, end_date = convert_date()
    date_generator = gen_date(start_date)
    logging.info(f"Начало работы синхронного приложения {datetime.datetime.now()}")
    time_now = datetime.datetime.now()
    db.create_db()

    while True:
        date = next(date_generator)  # Получаем следующую дату
        if date > end_date:  # Проверяем, не достигли ли мы конечной даты
            break
        loader = SyncLoader(date)

        table_info = loader.load()
        if not table_info:
            logging.info(f"Нет данных за {date.strftime('%d.%m.%Y')} г.")
            continue

        parser = ExcelParser(table_info)
        table = parser.table
        transform = DataTransformer(table, date)
        transfer_data_for_db = transform.transform()

        with uow.sync_start() as session:
            session.trading_results.add_all(transfer_data_for_db)
            logging.info(f"Загрузка информации в БД за {date.strftime("%d.%m.%Y")} г.")

    logging.info("Парсинг завершен")
    logging.info(f"Время работы приложения:{datetime.datetime.now() - time_now}")  # Время работы


if __name__ == "__main__":
    sync_main()
