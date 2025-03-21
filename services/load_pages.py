import requests


class LoadPages:
    """Класс для загрузки страниц по указанному URL."""

    def __init__(self, url_page: str, headers: dict = None):
        if headers is None:
            self.headers = {}
        self.url_page = url_page
        self.page_number = 1

    def download_html_page(self) -> str:
        """Скачивает страницу по-указанному URL и возвращает её текст."""

        response = requests.get(self.url_page, headers=self.headers)

        if response.status_code == 200:
            return response.content

    def load_next_page(self):
        """Загружает следующую страницу"""
        self.page_number += 1
        self.headers["page"] = f"page-{self.page_number}"
        return self.download_html_page()


