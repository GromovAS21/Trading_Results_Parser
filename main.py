import logging
from datetime import datetime
from services.html_page_parsers import BSParser
from services.load_pages import LoadPages
from func import convert_date, start_app

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

url = "https://spimex.com/markets/oil_products/trades/results/"

loader = LoadPages(url)
parser = BSParser()


def main():
    """Главная функция запуска приложения"""
    date_end = convert_date()
    logging.info("Начало работы приложения")  # Время работы
    time_now = datetime.now()
    start_app(loader, parser, date_end)  # Запуск приложения
    logging.info("Парсинг завершен")
    logging.info(f"Время работы приложения:{datetime.now() - time_now}")  # Время работы


if __name__ == '__main__':
    main()
