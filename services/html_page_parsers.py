from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, Tag

from abc_classes import HTMLParserInterface, DataSearchInterface
from services.load_pages import LoadPages


class BSParser(HTMLParserInterface):
    """Класс для парсинга данных с веб-страницы spimex.com"""

    def parse(self, html_page: str):
        return BeautifulSoup(html_page, 'html.parser')


class DataSearchBSParser(DataSearchInterface):
    """Класс для поиска данных на странице c с помощью BeautifulSoup"""

    def __init__(self, parse_page):
        self.__parse_page: BeautifulSoup = parse_page
        self.__table_info: List[Tag] = self._search_excel_table()

    def _search_excel_table(self) -> List[Tag]:
        """Поиск всей информации о Excel файлах на странице"""
        info_excel_tables_list = []
        info_found = self.__parse_page.select("div.accordeon-inner__wrap-item")

        if info_found:

            for data in info_found:

                if data.find(
                        "a",
                        class_="accordeon-inner__item-title link xls",
                        href=lambda x: "/upload/reports/" in x
                ):
                    info_excel_tables_list.append(data)
            return info_excel_tables_list

    def _search_dates(self) -> List[str]:
        """Поиск дат и создание списка дат"""
        date_list = []

        if self.__table_info:
            for info in self.__table_info:
                date = info.find("div", class_="accordeon-inner__item-inner__title").find("span").text
                date_format = datetime.strptime(date, "%d.%m.%Y").strftime("%d/%m//%Y")
                date_list.append(date_format)
        return date_list

    def _search_excel_links(self) -> List[str]:
        """Поиск всех ссылок на Excel файлы"""
        links_list = []

        if self.__table_info:
            domain_name = "https://spimex.com"
            for info in self.__table_info:
                link = info.find("a", class_="accordeon-inner__item-title link xls").get("href")
                links_list.append(f"{domain_name}{link}")

            return links_list

    def parse_data(self):
        """Сопоставление всех ссылок на Excel файлы и их дат"""

        date_list = self._search_dates()
        links_list = self._search_excel_links()

        if date_list and links_list and len(date_list) == len(links_list):
            urls_and_date = []
            for value in range(len(date_list)):
                urls_and_date.append((date_list[value], links_list[value]))
            return urls_and_date


if __name__ == '__main__':
    url = "https://spimex.com/markets/oil_products/trades/results/"
    load_page = LoadPages(url)
    html_page = load_page.download_html_page()
    parser = BSParser()
    data_parser = parser.parse(html_page)
    search_data_parser = DataSearchBSParser(data_parser)
    tables_item = search_data_parser.parse_data()
    print(tables_item)
