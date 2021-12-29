"""Модуль запуска приложения на локальном сервере разработки"""

from wsgiref.simple_server import make_server

from gentian_framework.gentian import GentianApplication
from urls import URLS
from middlewares import MIDDLEWARES


application = GentianApplication(URLS, MIDDLEWARES)

with make_server('', 8080, application) as dev_server:
    print("Приложение запущено на порту 8080...")
    dev_server.serve_forever()
