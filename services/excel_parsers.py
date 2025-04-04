import pandas as pd


class ExcelParser:
    """Класс для парсинга Excel-файлов."""

    def __init__(self, file_path):
        """Инициализирует экземпляр класса.

        Args:
            file_path (str): Путь к Excel-файлу.
        """
        self.file_path = file_path
        self._table = self.read_excel_file()
        self._rename_columns()
        self._filter_data()

    @property
    def table(self):
        """
        Возвращает DataFrame с нужными столбцами.

        Returns:
            pd.DataFrame: DataFrame с нужными столбцами.
        """
        return self._table

    def read_excel_file(self) -> pd.DataFrame:
        """
        Читает Excel-файл и возвращает DataFrame с нужными столбцами.

        Returns:
            pd.DataFrame: DataFrame с нужными столбцами.
        """
        return pd.read_excel(
            self.file_path,
            header=12,
            usecols=[1, 2, 3, 4, 5, 14]
        )

    def _rename_columns(self) -> None:
        """Переименовывает столбцы DataFrame."""
        self._table.columns = ["код_инструмента",
                               "наименование_инструмента",
                               "базис_поставки",
                               "объем_договора в единицах измерения",
                               "объем_договора",
                               "количество_договоров"
                               ]

    def _filter_data(self) -> None:
        """Фильтрует данные DataFrame."""
        self._table = self.table.loc[(self.table["количество_договоров"].str.strip() != "-") &
                                     (self.table["код_инструмента"].str.strip() not in ["Итого:", "Итого по секции:"])]
