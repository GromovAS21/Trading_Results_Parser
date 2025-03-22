import pandas as pd
from pandas import DataFrame


class DataTransformation:
    """Класс для преобразования данных"""

    def transform(self, data: DataFrame, date) -> dict:
        """Преобразование данных из DataFrame в нужные колонки для базы данных"""
        data_for_db = {}

        data_for_db['exchange_product_id'] = data['код_инструмента']
        data_for_db['exchange_product_name'] = data['наименование_инструмента']
        data_for_db['oil_id'] = data['код_инструмента'].str[:4]
        data_for_db['delivery_basis_id'] = data['код_инструмента'].str[4:7]
        data_for_db['delivery_basis_name'] = data['базис_поставки']
        data_for_db['delivery_type_id'] = data['код_инструмента'].str[-1]
        data_for_db['volume'] = data['объем_договора в единицах измерения']
        data_for_db['total'] = data['объем_договора']
        data_for_db['count'] = data['количество_договоров']
        data_for_db['date'] = date
        data_for_db['created_on'] = pd.to_datetime('now')
        data_for_db['updated_on'] = pd.to_datetime('now')
        return data_for_db