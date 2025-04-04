import datetime
from pathlib import Path
from typing import Generator, Optional

import requests


class LoadTable:
    """Класс для загрузки Exel таблицы c сайта spimex.com."""

    SITE_URL = "https://spimex.com/upload/reports/oil_xls/"

    def __init__(self, start_date, end_date):
        """
        Инициализация класса.

        Args:
            start_date (datetime.datetime): Начальная дата
            end_date (datetime.datetime): Конечная дата
        """
        self._start_date: datetime.datetime = start_date
        self._end_date: datetime.datetime = end_date
        self._table_date: Optional[datetime.datetime] = None
        self._date_generator: Generator = self._gen_date()
        self._path_file: Optional[Path] = None

    @property
    def path_file(self) -> Path:
        """
        Получение пути к файлу.

        Returns:
            Path: Путь к файлу
        """
        return self._path_file

    @property
    def table_date(self) -> datetime.datetime:
        """
        Получение текущей даты.

        Returns:
            datetime.datetime: Текущая дата
        """
        return self._table_date

    def _gen_date(self) -> Generator:
        """
        Генератор дат указанного диапазона.

        Returns:
            datetime.datetime: Дата для загрузки файла
        """
        current_date = self._start_date
        while current_date < self._end_date:
            yield current_date
            current_date += datetime.timedelta(days=1)

    def get_filename(self) -> str:
        """
        Формирует имя файла по заданной дате.

        Returns:
            str: Имя файла
        """
        filename = lambda x: "oil_xls_{}162000.xls".format(x.strftime("%Y%m%d"))
        self._table_date = next(self._date_generator)
        return filename(self._table_date)

    def load(self) -> bytes:
        """Загружает файл в папку по указанному адресу."""
        filename = self.get_filename()
        response = requests.get(self.SITE_URL + filename)
        if response.status_code == 200:
            return response.content
