"""Модуль стандартных классов представлений"""


class PageNotFound404:
    """Класс представления - страница не найдена"""

    def __call__(self, request):
        return '404 WHAT', '404 Page Not Found'

