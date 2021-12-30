"""Модуль шаблонизатора"""

from os.path import join

from jinja2 import Environment, FileSystemLoader


def render(template_name: str, folder: str = 'templates', static_url: str = '/static/', **kwargs) -> str:
    """
    Функция, отрисовывающая шаблон с параметрами
    :param static_url: путь к папке статики
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return: шаблон в строковом представлении
    """
    env = Environment()
    env.loader = FileSystemLoader(folder)
    env.globals['static'] = static_url
    template = env.get_template(template_name)
    return template.render(**kwargs)
