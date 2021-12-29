"""Основной модуль фреймворка"""

from typing import Callable

from gentian_framework.common_views import PageNotFound404


class GentianApplication:
    """Основной класс фреймворка"""

    def __init__(self, routes: dict, middlewares: list[Callable]):
        """
        Метод инициализации. Принимает списки путей и промежуточного ПО.
        :param routes: список путей для маршрутизации
        :param middlewares: список функций - промежуточного ПО, изменяющего содержание запросов
        """
        self.routes = routes
        self.middlewares = middlewares

    def __call__(self, environ: dict, start_response: Callable) -> list[bytes]:
        """
        Метод вызова объекта класса.
        :param environ: словарь параметров запроса
        :param start_response: обработчик, возвращающий ответ
        :return: Список байтовых строк
        """

        path = environ.get('PATH_INFO')
        view = PageNotFound404()

        if path:
            if not path.endswith('/'):
                path = f'{path}/'
            if path in self.routes:
                view = self.routes.get(path)

        request = dict()

        for middleware in self.middlewares:
            middleware(request)

        status_code, body = view(request)
        start_response(status_code, [('Content-Type', 'text/html')])

        return [body.encode('utf-8')]
