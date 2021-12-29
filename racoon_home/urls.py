"""
Модуль маршрутизации.

Импортируйте сюда необходимые представления и добавьте
из в словарь URLS с необходимыми адресами в качестве ключей.
"""

from views import IndexView, AboutView, ContactsView, CatalogView

URLS = {
    '/': IndexView(),
    '/about/': AboutView(),
    '/contacts/': ContactsView(),
    '/catalog/': CatalogView(),
}
