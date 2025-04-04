import datetime
from typing import List

import pandas as pd
from pandas import DataFrame

from db.models import TradingResults


class DataTransformation:
    """Класс для преобразования данных."""

    def __init__(self, data: DataFrame, date: datetime.datetime):
        """
        Инициализация класса DataTransformation.

        Args:
            data (DataFrame): Данные для преобразования.
            date (datetime.datetime): Дата, таблицы.
        """
        self.data = data
        self.date = date

    def transform(self) -> List[TradingResults]:
        """Преобразование данных из DataFrame в нужные колонки для базы данных."""
        data_for_db = []
        items = {}
        try:
            for _, row in self.data.iterrows():
                items["exchange_product_id"] = row["код_инструмента"]
                items["exchange_product_name"] = row["наименование_инструмента"]
                items["oil_id"] = row["код_инструмента"][:4]
                items["delivery_basis_id"] = row["код_инструмента"][4:7]
                items["delivery_basis_name"] = row["базис_поставки"]
                items["delivery_type_id"] = row["код_инструмента"][-1]
                items["volume"] = int(row["объем_договора в единицах измерения"])
                items["total"] = float(row["объем_договора"])
                items["count"] = int(row["количество_договоров"])
                items["date"] = self.date
                items["created_on"] = pd.to_datetime("now")
                items["updated_on"] = pd.to_datetime("now")
                trading_results_object = self._create_trading_results_object(items)
                data_for_db.append(trading_results_object)
        except (TypeError, ValueError):
            pass
        return data_for_db

    @staticmethod
    def _create_trading_results_object(data):
        """
        Функция для создания объекта TradingResults.

        Args:
            data (dict): Данные для создания объекта.

        Returns:
            TradingResults: Объект TradingResults.
        """
        return TradingResults(**data)
