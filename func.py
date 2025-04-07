import datetime
from typing import Iterator, Tuple


def convert_date() -> Tuple[datetime.date, datetime.date]:
    """
    Конвертация даты в формат datetime.date.

    Returns:
        start_date (datetime.date): Дата начала поиска
        end_date (datetime.date): Дата окончания поиска
    """
    while True:
        text = "Введите дату {} какой необходимо производить поиск (формат: ДД.ММ.ГГГГ): "
        start_date_input = input(text.format("c"))
        end_date_input = input(text.format("до"))
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


def gen_date(start_date: datetime.date) -> Iterator[datetime.date]:
    """
    Генератор дат указанного диапазона.

    Returns:
        Iterator[datetime.date]: Дата для загрузки файла
    """
    current_date = start_date

    while True:
        yield current_date
        current_date += datetime.timedelta(days=1)
