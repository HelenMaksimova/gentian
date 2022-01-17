"""Модуль запуска приложения на локальном сервере разработки"""

from wsgiref.simple_server import make_server

from gentian_framework.gentian import GentianApplication
from views import URLS
from middlewares import MIDDLEWARES
import settings as settings


application = GentianApplication(URLS, MIDDLEWARES, settings)

with make_server('', 8080, application) as dev_server:
    print("Приложение запущено на порту 8080...")
    try:
        dev_server.serve_forever()
    except KeyboardInterrupt:
        print("Приложение остановлено")
        exit(0)
