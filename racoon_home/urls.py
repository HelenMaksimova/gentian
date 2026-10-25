"""
Модуль маршрутизации.

Импортируйте сюда необходимые представления и добавьте
их в словарь URLS с необходимыми адресами в качестве ключей.
"""

from views import IndexView, AboutView, ContactsView, CatalogView, CreateCategoryView, CreateAnimalView, CopyAnimalView

URLS = {
    '/': IndexView(),
    '/about/': AboutView(),
    '/contacts/': ContactsView(),
    '/catalog/': CatalogView(),
    '/create_category/': CreateCategoryView(),
    '/create_animal/': CreateAnimalView(),
    '/copy_animal/': CopyAnimalView(),
}
