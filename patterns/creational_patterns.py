"""Модуль для классов порождающих паттернов"""
from copy import deepcopy
from quopri import decodestring


class BaseUser:
    pass


class Customer(BaseUser):
    pass


class Employee(BaseUser):
    pass


class Admin(BaseUser):
    pass


class UserFactory:
    types = {
        'customer': Customer,
        'employee': Employee,
        'admin': Admin,
    }

    @classmethod
    def create(cls, type_cls, *args, **kwargs):
        result_cls = cls.types.get(type_cls)
        if not result_cls:
            result_cls = list(cls.types.values())[-1].mro()[1]
        return result_cls(*args, **kwargs)


class AnimalPtototype:

    def clone(self):
        return deepcopy(self)


class Animal(AnimalPtototype):

    def __init__(self, name, age, category, description=None):
        self.name = name
        self.age = age
        self.category = category
        self.description = description
        self.category.animals.append(self)


class Raccoon(Animal):
    pass


class Ferret(Animal):
    pass


class Squirrel(Animal):
    pass


class AnimalFactory:
    types = {
        'raccoon': Raccoon,
        'ferret': Ferret,
        'squirrel': Squirrel,
    }

    @classmethod
    def create(cls, type_cls, *args, **kwargs):
        result_cls = cls.types.get(type_cls)
        if not result_cls:
            result_cls = list(cls.types.values())[-1].mro()[1]
        return result_cls(*args, **kwargs)


class Category:
    auto_id = 0

    def __init__(self, name, category=None):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.animals = []

    def animal_count(self):
        result = len(self.animals)
        if self.category:
            result += self.category.animal_count()
        return result


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        name = args[0] if args else kwargs.get('name')

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)


class Engine:
    def __init__(self):
        self.factory = AnimalFactory
        self.employeers = []
        self.customers = []
        self.admins = []
        self.animals = []
        self.categories = []

    def get_factory_types(self):
        return list(self.factory.types.keys())

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, category_id):
        for item in self.categories:
            if item.id == category_id:
                return item
        return

    def create_animal(self, type_cls, name, age, category, description):
        animal = self.factory.create(type_cls, name, age, category, description)
        self.animals.append(animal)
        return animal

    def get_animal(self, name):
        for item in self.animals:
            if item.name == name:
                return item
        return

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')
