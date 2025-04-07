import datetime

import aiohttp
import requests

from abc_classes import AbstractLoader


class SyncLoader(AbstractLoader):
    """Класс для синхронной загрузки Exel таблицы c сайта spimex.com."""

    SITE_URL = "https://spimex.com/upload/reports/oil_xls/"

    def __init__(self, current_date: datetime.date):
        """
        Инициализация класса.

        Args:
            current_date (datetime.datetime): Текущая дата
        """
        self._current_date: datetime.date = current_date

    def _get_filename(self) -> str:
        """
        Формирует имя файла по заданной дате.

        Returns:
            str: Имя файла
        """
        filename = lambda x: "oil_xls_{}162000.xls".format(x.strftime("%Y%m%d"))
        return filename(self._current_date)

    def load(self) -> bytes:
        """
        Синхронно загружает файл по указанному адресу.

        Returns:
            bytes
        """
        filename = self._get_filename()
        response = requests.get(self.SITE_URL + filename)
        if response.status_code == 200:
            return response.content


class AsyncLoader(SyncLoader):
    """Класс для aсинхронной загрузки Exel таблицы c сайта spimex.com."""

    async def load(self) -> bytes:
        """
        Асинхронно загружает файл по указанному адресу.

        Returns:
            bytes: Содержимое файла
        """
        filename = self._get_filename()
        async with aiohttp.ClientSession() as session:
            async with session.get(self.SITE_URL + filename) as response:
                if response.status == 200:
                    return await response.read()
