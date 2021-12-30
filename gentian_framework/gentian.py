"""Основной модуль фреймворка"""

from typing import Callable, List

from gentian_framework.common_views import PageNotFound404
from gentian_framework.utils import RequestProcessors, get_content_type, get_static


class GentianApplication:
    """Основной класс фреймворка"""

    REQUEST_PROCESSORS = {
        'GET': RequestProcessors.get_method_process,
        'POST': RequestProcessors.post_method_process,
    }

    def __init__(self, routes: dict, middlewares: List[Callable], settings):
        """
        Метод инициализации. Принимает списки путей и промежуточного ПО.
        :param routes: список путей для маршрутизации
        :param middlewares: список функций - промежуточного ПО, изменяющего содержание запросов
        """
        self.routes = routes
        self.middlewares = middlewares
        self.settings = settings

    def __call__(self, environ: dict, start_response: Callable) -> List[bytes]:
        """
        Метод вызова объекта класса.
        :param environ: словарь параметров запроса
        :param start_response: обработчик, возвращающий ответ
        :return: Список байтовых строк
        """

        path = environ.get('PATH_INFO')
        method = environ.get('REQUEST_METHOD')

        request = dict()

        for middleware in self.middlewares:
            middleware(request)

        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.routes:
            view = self.routes[path]
            content_type = get_content_type(path)
            status_code, body = view(request)
            body = body.encode('utf-8')

        elif path.startswith(self.settings.STATIC_URL):
            file_path = path[len(self.settings.STATIC_URL):len(path) - 1]
            content_type = get_content_type(file_path)
            status_code, body = get_static(self.settings.STATIC_FILES_DIR, file_path)

        else:
            view = PageNotFound404()
            content_type = get_content_type(path)
            status_code, body = view(request)
            body = body.encode('utf-8')

        if method in self.REQUEST_PROCESSORS:
            request['method'] = method
            self.REQUEST_PROCESSORS[method](environ, request)

        start_response(status_code, [('Content-Type', content_type)])

        return [body]
