"""
Модуль представлений

Добавьте сюда представления для каждой страницы в виде вызываемых объектов,
возвращающих код ответа в виде строки и результат выполнения функции render.
В функцию render необходимо передать имя шаблона, при необходимости можно
передать параметры.
"""


from gentian_framework.templator import render


class IndexView:
    """Класс представления для главной страницы"""
    def __call__(self, request):
        context = {
            'date': request.get('date'),
            'city': request.get('city'),
        }
        return '200 OK', render('index.html', **context)


class AboutView:
    """Класс представления для страницы О нас"""
    def __call__(self, request):
        context = {
            'date': request.get('date'),
            'city': request.get('city'),
        }
        return '200 OK', render('about.html', **context)


class ContactsView:
    """Класс представления для страницы контактов"""
    def __call__(self, request):
        context = {
            'date': request.get('date'),
            'city': request.get('city'),
        }
        return '200 OK', render('contacts.html', **context)


class CatalogView:
    """Класс представления для страницы каталога"""
    def __call__(self, request):
        context = {
            'racoons': ['Вася', 'Петя', 'Маша'],
            'date': request.get('date'),
            'city': request.get('city'),
        }
        return '200 OK', render('catalog.html', **context)
