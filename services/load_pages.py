import requests


class LoadPages:
    """Класс для загрузки страниц по указанному URL."""

    def __init__(self, url_page: str):
        self._url_page = url_page
        self._headers = {}
        self._page_number = 1
        self._headers["page"] = f"page-{self._page_number}"

    @property
    def page_number(self):
        return self._page_number

    @page_number.setter
    def page_number(self, number):
        self._page_number += number

    def download_html_page(self) -> str:
        """Скачивает страницу по-указанному URL и возвращает её текст."""

        try:
            response = requests.get(self._url_page, headers=self._headers)
            return response.text
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Указан неверный url")