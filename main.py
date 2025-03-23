import logging
import timeit
from datetime import datetime
from database import create_db
from services.html_page_parsers import BSParser
from services.load_pages import LoadPages
from func import convert_date, start_app
from models import TradingResults

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

url = "https://spimex.com/markets/oil_products/trades/results/"
date_end = convert_date("01.01.2023")

loader = LoadPages(url)
parser = BSParser()


if __name__ == '__main__':
    time_now = datetime.now()
    create_db() # Создание таблицы в бд
    start_app(loader, parser, date_end) # Запуск приложения
    logging.info(datetime.now() - time_now) # Время работы

