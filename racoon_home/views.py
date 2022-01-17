"""
Модуль представлений

Добавьте сюда представления для каждой страницы в виде вызываемых объектов,
возвращающих код ответа в виде строки и результат выполнения функции render.
В функцию render необходимо передать имя шаблона, при необходимости можно
передать параметры.
"""
import datetime

from gentian_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import route, debug, AppRoute, Debug

site = Engine()
LOG = Logger('views_log')

URLS = {}


@route(URLS, '/')
class IndexView:
    """Класс представления для главной страницы"""

    @debug
    def __call__(self, request):
        context = {
            'date': request.get('date'),
            'city': request.get('city'),
        }
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен request: {request}')
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен context: {context}')
        return '200 OK', render('index.html', **context)


@route(URLS, '/about/')
class AboutView:
    """Класс представления для страницы О нас"""

    @debug
    def __call__(self, request):
        context = {
            'date': request.get('date'),
            'city': request.get('city'),
        }
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен request: {request}')
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен context: {context}')
        return '200 OK', render('about.html', **context)


@route(URLS, '/contacts/')
class ContactsView:
    """Класс представления для страницы контактов"""

    @debug
    def __call__(self, request):
        context = {
            'date': request.get('date'),
            'city': request.get('city'),
        }
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен request: {request}')
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен context: {context}')
        return '200 OK', render('contacts.html', **context)


@AppRoute(URLS, '/catalog/')
class CatalogView:
    """Класс представления для страницы каталога"""

    @Debug()
    def __call__(self, request):
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
        except KeyError:
            category = None
        animals = site.animals if not category else category.animals
        category_name = 'Все питомцы' if not category else category.name
        count = len(site.animals) if not category else category.animal_count()
        context = {
            'objects_list': animals,
            'categories': site.categories,
            'count': count,
            'category_name': category_name,
            'category': category,
            'date': request.get('date'),
            'city': request.get('city'),
        }
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен request: {request}')
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен context: {context}')
        return '200 OK', render('catalog.html', **context)


@AppRoute(URLS, '/create_category')
class CreateCategoryView:
    """Класс представления для страницы создания новой категории"""

    @Debug()
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получены данные POST-запроса: {data}')
            name = site.decode_value(data['name'])
            category_id = data.get('category_id')
            category = site.find_category_by_id(int(category_id)) if category_id else None

            new_category = site.create_category(name, category)
            site.categories.append(new_category)
        context = {
            'categories': site.categories
        }
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен request: {request}')
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен context: {context}')
        return '200 OK', render('create_category.html', **context)


@AppRoute(URLS, '/create_animal/')
class CreateAnimalView:
    """Класс представления для страницы создания новой карточки питомца"""

    @Debug()
    def __call__(self, request):
        context = {
            'categories': site.categories,
            'category': None
        }
        if request['method'] == 'POST':
            data = request['data']
            LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получены данные POST-запроса: {data}')
            data.update({
                'category': site.find_category_by_id(int(data['category'])),
                'name': site.decode_value(data['name']),
                'age': int(data['age']),
                'description': site.decode_value(data['description'])
            })
            site.create_animal(**data)
            request['request_params'] = {'id': data['category'].id}
            LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен request: {request}')
            LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен context: {context}')
            LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: '
                    f'выполнено перенаправление на view: {CatalogView.__name__}')
            return CatalogView()(request)
        else:
            category = site.find_category_by_id(int(request['request_params']['id']))
            context.update({
                'animal_types': site.get_factory_types(),
                'category': category
            })
            LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен request: {request}')
            LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен context: {context}')
            return '200 OK', render('create_animal.html', **context)


@AppRoute(URLS, '/copy_animal/')
class CopyAnimalView:
    """Класс представления для страницы копирования карточки питомца"""

    @Debug()
    def __call__(self, request):
        name = request['request_params'].get('name')
        animal = site.get_animal(name)
        if animal:
            new_animal = animal.clone()
            new_animal.name = f'copy_{animal.name}'
            new_animal.category = animal.category
            new_animal.category.animals.append(new_animal)
            site.animals.append(new_animal)
        request['request_params'] = {'id': animal.category.id}
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен request: {request}')
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: '
                f'выполнено перенаправление на view: {CatalogView.__name__}')
        return CatalogView()(request)
