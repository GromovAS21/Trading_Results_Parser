import requests


class LoadPages:
    """Класс для загрузки страниц по указанному URL"""

    def __init__(self, url_page: str):
        self._base_url = url_page
        self.headers = {}
        self._page_number = 1

    @property
    def page_number(self):
        return self._page_number

    @page_number.setter
    def page_number(self, number):
        self._page_number = number

    def get_url_with_page(self):
        """Формирует URL с текущим номером страницы"""
        return f"{self._base_url}?page=page-{self._page_number}"

    def download_html_page(self) -> str:
        """Скачивает страницу по-указанному URL и возвращает её текст"""
        try:
            response = requests.get(self.get_url_with_page())
            return response.text
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Указан неверный url")