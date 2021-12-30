"""Основной модуль фреймворка"""

from typing import Callable, List

from gentian_framework.common_views import PageNotFound404
from gentian_framework.utils import RequestProcessors


class GentianApplication:
    """Основной класс фреймворка"""

    REQUEST_PROCESSORS = {
        'GET': RequestProcessors.get_method_process,
        'POST': RequestProcessors.post_method_process,
    }

    def __init__(self, routes: dict, middlewares: List[Callable]):
        """
        Метод инициализации. Принимает списки путей и промежуточного ПО.
        :param routes: список путей для маршрутизации
        :param middlewares: список функций - промежуточного ПО, изменяющего содержание запросов
        """
        self.routes = routes
        self.middlewares = middlewares

    def __call__(self, environ: dict, start_response: Callable) -> List[bytes]:
        """
        Метод вызова объекта класса.
        :param environ: словарь параметров запроса
        :param start_response: обработчик, возвращающий ответ
        :return: Список байтовых строк
        """

        path = environ.get('PATH_INFO')
        method = environ.get('REQUEST_METHOD')
        view = PageNotFound404()

        if path:
            if not path.endswith('/'):
                path = f'{path}/'
            if path in self.routes:
                view = self.routes.get(path)

        request = dict()

        for middleware in self.middlewares:
            middleware(request)

        if method in self.REQUEST_PROCESSORS:
            request['method'] = method
            self.REQUEST_PROCESSORS[method](environ, request)

        status_code, body = view(request)
        start_response(status_code, [('Content-Type', 'text/html')])

        return [body.encode('utf-8')]
