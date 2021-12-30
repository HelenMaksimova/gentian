"""Модуль утилит"""

from quopri import decodestring
from os import path

from gentian_framework.source.content_types import CONTENT_TYPES_MAP


def parse_input_data(data: str) -> dict:
    """Функция, выполняющая парсинг параметров из запроса в словарь"""
    try:
        result = dict((item.split('=') for item in data.split('&'))) if data else {}
    except ValueError as error:
        print(error)
        result = {}
    return result


def decode_value(data: dict) -> dict:
    """Функция для преобразования данных из запросов в корректную кодировку"""
    new_data = {}
    for k, v in data.items():
        val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val).decode('UTF-8')
        new_data[k] = val_decode_str
    return new_data


def get_content_type(file_path: str, content_types_map: dict = CONTENT_TYPES_MAP) -> str:
    """Функция возвращает тип контента в зависимости от расширения файла"""
    file_name = path.basename(file_path).lower()
    extension = path.splitext(file_name)[1]
    return content_types_map.get(extension, "text/html")


def get_static(static_dir: str, file_path: str) -> tuple:
    """Функция возвращает кортеж из статус-кода в формате строки и контента файла в формате байт"""
    path_to_file = path.join(static_dir, file_path)
    with open(path_to_file, 'rb') as f:
        file_content = f.read()
    status_code = '200 OK'
    return status_code, file_content


class GetRequests:
    """Класс, объединяющий методы для get-запросов"""

    @staticmethod
    def get_request_params(environ: dict) -> dict:
        """Метод для получения словаря параметров из строки запроса"""
        query_string = environ['QUERY_STRING']
        request_params = parse_input_data(query_string)
        return request_params


class PostRequests:
    """Класс, объединяющий методы для post-запросов"""

    @staticmethod
    def get_wsgi_input_data(environ: dict) -> bytes:
        """Метод для преобразования тела запроса в байты"""
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    @staticmethod
    def parse_wsgi_input_data(data: bytes) -> dict:
        """Метод для получения из байтовой строки словаря с данными"""
        result = parse_input_data(data.decode(encoding='utf-8')) if data else {}
        return result

    def get_request_params(self, environ: dict) -> dict:
        """Метод для получения словаря данных"""
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        return data


class RequestProcessors:
    """Класс, объединяющий методы для обработки запросов"""

    @staticmethod
    def get_method_process(environ: dict, request: dict):
        """Метод-обработчик GET-запроса"""
        request_params = GetRequests().get_request_params(environ)
        request['request_params'] = decode_value(request_params)
        print(f'Нам пришли GET-параметры: {request["request_params"]}')

    @staticmethod
    def post_method_process(environ: dict, request: dict):
        """Метод-обработчик POST-запроса"""
        data = PostRequests().get_request_params(environ)
        request['data'] = decode_value(data)
        print(f'Нам пришёл post-запрос: {request["data"]}')
