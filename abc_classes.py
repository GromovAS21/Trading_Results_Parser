from abc import abstractmethod, ABC


class HTMLParserInterface(ABC):
    """Абстрактный класс для парсинга данных"""

    @abstractmethod
    def parse(self, html_page: str):
        pass


class DataSearchInterface(ABC):
    """Абстрактный класс для поиска данных на странице"""

    @abstractmethod
    def _search_excel_table(self):
        """Поиск всей информации о Excel файлах на странице"""
        pass

    @abstractmethod
    def _search_dates(self):
        """Поиск всех дат у Excel файлах"""
        pass

    @abstractmethod
    def _search_excel_links(self):
        """Поиск всех ссылко на Excel файлы"""
        pass

    @abstractmethod
    def parse_data(self):
        """Вывод результата"""
        pass
