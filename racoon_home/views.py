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
from patterns.structural_patterns import route, debug, AppRoute
from gentian_framework.common_views import CreateView, ListView
from patterns.behavioral_patterns import SmsNotifier, EmailNotifier

site = Engine()
LOG = Logger('views_log')
observers = [SmsNotifier(), EmailNotifier()]

URLS = {}


@route(URLS, '/')
class IndexView:
    """Класс представления для главной страницы"""

    @debug
    def __call__(self, request):
        context = {
            'date': request.get('date'),
            'city': request.get('city'),
            'user': site.current_user,
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
            'user': site.current_user,
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
            'user': site.current_user,
        }
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен request: {request}')
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен context: {context}')
        return '200 OK', render('contacts.html', **context)


class CatalogView:
    """Класс представления для страницы каталога"""

    @debug
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
            'user': site.current_user,
        }
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен request: {request}')
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен context: {context}')
        return '200 OK', render('catalog.html', **context)


@AppRoute(URLS, '/create_category/')
class CreateCategoryView:
    """Класс представления для страницы создания новой категории"""

    @debug
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
            'categories': site.categories,
            'date': request.get('date'),
            'city': request.get('city'),
            'user': site.current_user,
        }
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен request: {request}')
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен context: {context}')
        return '200 OK', render('create_category.html', **context)


@AppRoute(URLS, '/create_animal/')
class CreateAnimalView:
    """Класс представления для страницы создания новой карточки питомца"""

    @debug
    def __call__(self, request):
        context = {
            'date': request.get('date'),
            'city': request.get('city'),
            'categories': site.categories,
            'category': None,
            'user': site.current_user
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
            animal = site.create_animal(**data)
            animal.add_observers(observers)
            request['request_params'] = {'id': data['category'].id}
            LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен request: {request}')
            LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен context: {context}')
            LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: '
                    f'выполнено перенаправление на view: CatalogView')
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

    @debug
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
                f'выполнено перенаправление на view CatalogView')
        return CatalogView()(request)


class CustomersListView(ListView):
    template_name = 'users.html'

    def get_queryset(self):
        return site.customers

    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'user': site.current_user
        })
        return context


class CustomerCreateView(CreateView):
    template_name = 'create_user.html'

    def create_object(self, data):
        data.update({
            'first_name': site.decode_value(data.get('first_name')),
            'last_name': site.decode_value(data.get('last_name')),
        })
        site.create_customer(**data)

    def get_context_data(self):
        context = {
            'user': site.current_user
        }
        return context


class LoginView(CreateView):
    template_name = 'login_user.html'

    def create_object(self, data):
        user_id = int(data.get('user_id'))
        site.current_user = site.find_customer_by_id(user_id)

    def get_context_data(self):
        context = {
            'user': site.current_user,
            'users': site.customers,
        }
        return context


class OrderAnimalView:
    def __call__(self, request):
        name = request['request_params'].get('name')
        animal = site.get_animal(name)
        customer = site.current_user
        if animal:
            animal.add_customer(customer)
        request['request_params'] = {'id': animal.category.id}
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: получен request: {request}')
        LOG.log(f'{datetime.datetime.now()}: {self.__class__.__name__}: '
                f'выполнено перенаправление на view CatalogView')
        return CatalogView()(request)


URLS.update({
    '/catalog/': CatalogView(),
    '/customers/': CustomersListView(),
    '/create_customer/': CustomerCreateView(),
    '/order_animal/': OrderAnimalView(),
    '/login/': LoginView(),
})
