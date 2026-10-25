"""Модуль для классов порождающих паттернов"""
from copy import deepcopy
from quopri import decodestring

from patterns.behavioral_patterns import Subject, SmsNotifier, EmailNotifier, FileWriter


class BaseUser:

    auto_id = 0

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.id = self.auto_id
        self.increment_id()

    def __str__(self):
        return self.fullname

    @classmethod
    def increment_id(cls):
        cls.auto_id += 1

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'


class Customer(BaseUser):
    def __init__(self, first_name, last_name):
        super().__init__(first_name, last_name)
        self.orders = []

    def __getitem__(self, idx):
        return self.orders[idx]

    def __iter__(self):
        for item in self.orders:
            yield item


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


class Animal(AnimalPtototype, Subject):

    def __init__(self, name, age=1, category=None, description=None):
        super().__init__()
        self.name = name
        self.age = age
        self.category = category
        self.description = description
        if self.category:
            self.category.animals.append(self)
        self.customers = []

    def __str__(self):
        return self.name

    def __getitem__(self, idx):
        return self.customers[idx]

    def __iter__(self):
        for item in self.customers:
            yield item

    def add_customer(self, customer):
        self.customers.append(customer)
        customer.orders.append(self)
        self.notify()


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

    def __getitem__(self, idx):
        return self.animals[idx]

    def __iter__(self):
        for item in self.animals:
            yield item


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs, **kwargs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        name = args[0] if args else kwargs.get('name')

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        self.writer.write(text)


class Engine:
    def __init__(self):
        self.factory = AnimalFactory
        self.current_user = None
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

    def find_customer_by_id(self, customer_id):
        for item in self.customers:
            if item.id == customer_id:
                return item
        return

    def create_animal(self, type_cls, name, age, category, description):
        animal = self.factory.create(type_cls, name, age, category, description)
        self.animals.append(animal)
        return animal

    def create_customer(self, first_name, last_name):
        customer = Customer(first_name, last_name)
        self.customers.append(customer)
        print(self.customers)
        return customer

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


if __name__ == '__main__':

    customers = [Customer(f'customer_{num:02}', f'customer_{num:02}') for num in range(1, 11)]
    email_nt = EmailNotifier()
    sms_nt = SmsNotifier()
    animal_01 = Animal('animal_01')
    animal_01.add_observers((email_nt, sms_nt))
    animal_02 = Animal('animal_02')
    animal_02.add_observers((email_nt, sms_nt))
    for customer_ in customers:
        animal_01.add_customer(customer_)
        animal_02.add_customer(customer_)

    for item_ in animal_01:
        print(item_)

    print()

    for item_ in animal_02:
        print(item_)

    print()

    for item_ in customers[0]:
        print(item_)

    print()

    print(animal_01[0])
    print(customers[0][0])
