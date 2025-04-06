import datetime
from typing import Iterator


def convert_date():
    """
    Конвертация даты в формат datetime.date.

    Returns:
        start_date (datetime.date): Дата начала поиска
        end_date (datetime.date): Дата окончания поиска
    """
    while True:
        start_date_input = input("Введите дату c какой необходимо производить поиск (формат: ДД.ММ.ГГГГ): ")
        end_date_input = input("Введите дату до какой необходимо производить поиск (формат: ДД.ММ.ГГГГ): ")
        try:
            start_date, end_date = tuple(
                map(lambda x: datetime.datetime.strptime(x, "%d.%m.%Y").date(), (start_date_input, end_date_input))
            )

            if start_date > end_date or end_date > datetime.date.today():
                print("Некорректный диапазон дат")
                continue

            else:
                return start_date, end_date

        except ValueError:
            print("Некорректный формат даты: Введите дату в формате: ДД.ММ.ГГГГ")


def gen_date(start_date: datetime.datetime) -> Iterator[datetime.datetime]:
    """
    Генератор дат указанного диапазона.

    Returns:
        Iterator[datetime.datetime]: Дата для загрузки файла
    """
    current_date = start_date
    while True:
        yield current_date
        current_date += datetime.timedelta(days=1)
