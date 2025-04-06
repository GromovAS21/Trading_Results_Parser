import datetime
from pathlib import Path
from typing import Optional

import aiohttp
import requests


class LoadTable:
    """Класс для загрузки Exel таблицы c сайта spimex.com."""

    SITE_URL = "https://spimex.com/upload/reports/oil_xls/"

    def __init__(self, current_date: datetime.datetime):
        """
        Инициализация класса.

        Args:
            current_date (datetime.datetime): Текущая дата
        """
        self._current_date: datetime.datetime = current_date
        self._table_date: Optional[datetime.datetime] = None
        self._path_file: Optional[Path] = None

    @property
    def path_file(self) -> Path:
        """
        Получение пути к файлу.

        Returns:
            Path: Путь к файлу
        """
        return self._path_file

    def get_filename(self) -> str:
        """
        Формирует имя файла по заданной дате.

        Returns:
            str: Имя файла
        """
        filename = lambda x: "oil_xls_{}162000.xls".format(x.strftime("%Y%m%d"))
        return filename(self._current_date)

    def sync_load(self) -> bytes:
        """Синхронно загружает файл по указанному адресу."""
        filename = self.get_filename()
        response = requests.get(self.SITE_URL + filename)
        if response.status_code == 200:
            return response.content

    async def async_load(self) -> bytes:
        """Асинхронно загружает файл по указанному адресу."""
        filename = self.get_filename()
        async with aiohttp.ClientSession() as session:
            async with session.get(self.SITE_URL + filename) as response:
                if response.status == 200:
                    return await response.read()
