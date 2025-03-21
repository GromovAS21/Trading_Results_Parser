from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, ResultSet, Tag

from services.load_pages import LoadPages


class HTMLParser:
    """Класс для парсинга данных с веб-страницы spimex.com"""

    def __init__(self, html_page: str):
        self._html_page = html_page

    def parse_html_page(self) -> BeautifulSoup:
        """Парсинг данных с веб-страницы."""
        parse_page = BeautifulSoup(self._html_page, 'html.parser')
        return parse_page

    def search_exel_table(self, parse_page: BeautifulSoup) -> List[Tag]:
        """Поиск всех информации о Excel файлах на странице"""
        info_excel_tables_list = []
        info_found = parse_page.select("div.accordeon-inner__wrap-item")

        if info_found:

            for data in info_found:

                if data.find(
                        "a",
                        class_="accordeon-inner__item-title link xls",
                        href=lambda x: "/upload/reports/" in x
                ):
                    info_excel_tables_list.append(data)
        return info_excel_tables_list

    @staticmethod
    def _search_dates(info_list: List[ResultSet]) -> List[str]:
        """Поиск дат и создание списка дат"""
        date_list = []

        if info_list:
            for info in info_list:
                date = info.find("div", class_="accordeon-inner__item-inner__title").find("span").text
                date_format = datetime.strptime(date, "%d.%m.%Y").strftime("%d/%m//%Y")
                date_list.append(date_format)
        return date_list

    @staticmethod
    def _search_excel_links(info_list: List[ResultSet]) -> List[str]:
        """Поиск всех ссылко на Excel файлы"""
        links_list = []

        if info_list:
            domain_name = "https://spimex.com"
            for info in info_list:
                link = info.find("a", class_="accordeon-inner__item-title link xls").get("href")
                links_list.append(f"{domain_name}{link}")

            return links_list

    def excel_links_and_dates(self, parse_page):
        """Сопоставление всех ссылок на Excel файлы и их дат"""

        date_list = self._search_dates(parse_page)
        links_list = self._search_excel_links(parse_page)

        if len(date_list) == len(links_list) and date_list and links_list:
            urls_and_date = []
            for value in range(len(date_list)):
                urls_and_date.append((date_list[value], links_list[value]))
            return urls_and_date


if __name__ == '__main__':
    url = "https://spimex.com/markets/oil_products/trades/results/"
    load_page = LoadPages(url)
    html_page = load_page.download_html_page()
    parser = HTMLParser(html_page)
    parse_page = parser.parse_html_page()
    search_exel_table = parser.search_exel_table(parse_page)
    a = parser.excel_links_and_dates(search_exel_table)
    print(a)
