import pandas as pd


class ExcelParser:
    """Класс для парсинга Excel-файлов."""

    def __init__(self, url_excel):
        self._url_excel = url_excel
        self._table = self.load_excel_file()
        self._rename_columns()
        self._filter_data()

    @property
    def table(self):
        return self._table

    def load_excel_file(self) -> pd.DataFrame:
        """Читает Excel-файл и возвращает DataFrame с нужными столбцами"""
        return pd.read_excel(self._url_excel, header=12, usecols=[1, 2, 3, 4, 5, 14])

    def _rename_columns(self) -> None:
        """Переименовывает столбцы DataFrame."""
        self._table.columns = ["код_инструмента", "наименование_инструмента", "базис_поставки",
                               "объем_договора в единицах измерения", "объем_договора", "количество_договоров"
                               ]

    def _filter_data(self) -> None:
        """Фильтрует данные DataFrame от строк, где количество договоров равно 0"""
        self._table = self.table.loc[self.table["количество_договоров"].str.strip() != "-"]
