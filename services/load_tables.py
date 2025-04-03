import datetime
from pathlib import Path

import requests


class LoadTable:
    """Класс для загрузки Exel таблицы c сайта spimex.com"""

    SITE_URL = "https://spimex.com/upload/reports/oil_xls/"

    def __init__(self, start_date, end_date):
        self._start_date = start_date
        self._end_date = end_date
        self._current_date = self.gen_date()

    def gen_date(self):
        """Генератор дат указанного диапазона"""
        current_date = self._start_date
        while True:
            try:
                if not current_date > self._end_date:
                    yield current_date
                    current_date += datetime.timedelta(days=1)
            except StopIteration:
                break

    def get_filename(self):
        """Формирует имя файла по заданной дате"""
        filename = lambda x: "oil_xls_{}162000.xls".format(x.strftime("%Y%m%d"))
        return filename(next(self._current_date))

    def load_table(self):
        """Загружает файл по указанному адресу"""
        filename = self.get_filename()
        request = requests.get(self.SITE_URL + filename)
        if request.status_code == 200:
            self.save_table(request, filename)

    @staticmethod
    def save_table(request, filename):
        path_file = Path("../load_table").joinpath(filename)
        with open(path_file, "wb") as file:
            file.write(request.content)
