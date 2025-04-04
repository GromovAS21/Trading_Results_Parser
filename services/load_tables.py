import datetime
from pathlib import Path
from typing import Generator, Optional

import requests


class LoadTable:
    """
    Класс для загрузки Exel таблицы c сайта spimex.com.
    """

    SITE_URL = "https://spimex.com/upload/reports/oil_xls/"

    def __init__(self, start_date, end_date):
        self._start_date: datetime.datetime = start_date
        self._end_date: datetime.datetime = end_date
        self._current_date: Generator = self._gen_date()
        self._path_file: Optional[Path] = None

    @property
    def get_path_file(self) -> Path:
        """Получение пути к файлу."""
        return self._path_file

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
        return filename(next(self._current_date))

    def load(self) -> None:
        """
        Загружает файл в папку по указанному адресу.
        """
        filename = self.get_filename()
        request = requests.get(self.SITE_URL + filename)
        if request.status_code == 200:
            self.save(request, filename)

    def save(self, request: requests.models.Response, filename: str) -> None:
        """
        Сохраняет файл по указанному пути возвращает путь к файлу.

        Args:
            request (requests.models.Response): Ответ от сервера
            filename (str): Имя файла
        """
        self._path_file = Path(__file__).parent.parent / "load_table" / filename
        with open(self._path_file, "wb") as file:
            file.write(request.content)


if __name__ == "__main__":
    loader = LoadTable(datetime.datetime(2023, 1, 1), datetime.datetime.today())
    while True:
        loader.load()



