import logging
from datetime import datetime
from database import Session
from services.data_transformation import DataTransformation
from services.excel_parsers import ExcelParser
from services.html_page_parsers import DataSearchBSParser
from uow import UnitOfWork

uow = UnitOfWork(session_factory=Session())
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def convert_date(date: str):
    """Конвертация даты в формат datetime.date"""
    try:
        return datetime.strptime(date, "%d.%m.%Y").date()
    except ValueError:
        raise ValueError("Некорректный формат даты: Введите дату в формате: ДД.ММ.ГГГГ")


def start_app(loader, html_parser, date_end):
    """Функция для запуска приложения"""
    while True:
        html_page = loader.download_html_page()  # Загрузка страницы
        parse_page = html_parser.parse(html_page)  # Парсинг страницы
        search = DataSearchBSParser(parse_page)  # Поиск информации о таблицах на странице
        parse_data = search.parse_data()  # Сбор информации о ссылки на таблицу и дате

        counter = True

        for data in parse_data:

            if data[0] > date_end:
                excel_table = ExcelParser(data[1])
                transformation = DataTransformation()
                data_trans = transformation.transform(excel_table.table, data[0])
                logging.info(f"Парсинг таблицы от {data[0].strftime('%d.%m.%Y')} года")

                with uow.start() as session:
                    session.trading_results.add_all(data_trans)
            else:
                counter = False
                logging.info("Парсинг завершен")
                break

        if not counter:
            break

        loader.page_number += 1
