from typing import List

import pandas as pd
from pandas import DataFrame


class DataTransformation:
    """Класс для преобразования данных"""

    @staticmethod
    def transform(data: DataFrame, date) -> List[dict]:
        """Преобразование данных из DataFrame в нужные колонки для базы данных"""
        data_for_db = []
        items = {}
        try:
            for idx, row in data.iterrows():
                items['exchange_product_id'] = row['код_инструмента']
                items['exchange_product_name'] = row['наименование_инструмента']
                items['oil_id'] = row['код_инструмента'][:4]
                items['delivery_basis_id'] = row['код_инструмента'][4:7]
                items['delivery_basis_name'] = row['базис_поставки']
                items['delivery_type_id'] = row['код_инструмента'][-1]
                items['volume'] = row['объем_договора в единицах измерения']
                items['total'] = row['объем_договора']
                items['count'] = row['количество_договоров']
                items['date'] = date
                items['created_on'] = pd.to_datetime('now')
                items['updated_on'] = pd.to_datetime('now')
                data_for_db.append(items)
        except TypeError:
            pass
        return data_for_db