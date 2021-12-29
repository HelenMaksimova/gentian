"""
Модуль промежуточного ПО

Напишите здесь функции, изменяющие request
"""

from datetime import date


def current_date(request: dict):
    """Функция добавляет текущую дату"""
    request['date'] = date.today()


def current_city(request: dict):
    """Функция добавляет город"""
    request['city'] = 'Москва'


MIDDLEWARES = [
    current_date,
    current_city,
]
