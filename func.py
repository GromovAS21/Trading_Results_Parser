from datetime import datetime


def convert_date(date: str):
    """Конвертация даты в формат datetime.date"""
    return datetime.strptime(date, "%d.%m.%Y").date()