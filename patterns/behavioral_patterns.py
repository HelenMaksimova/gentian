import json


class Observer:

    def update(self, subject):
        pass


class Subject:

    def __init__(self):
        self.observers = []

    def add_observers(self, observers):
        self.observers.extend(observers)

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):

    def update(self, subject):
        print(f'SMS: {subject[-1].fullname} выбрал питомца {subject.name}')


class EmailNotifier(Observer):

    def update(self, subject):
        print(f'E-MAIL: {subject[-1].fullname} выбрал питомца {subject.name}')


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return json.dumps(self.obj)

    @staticmethod
    def load(data):
        return json.loads(data)


class Writer:

    def write(self, text):
        pass


class ConsoleWriter(Writer):

    def write(self, text):
        print(text)


class FileWriter(Writer):

    def __init__(self, file_name='log'):
        self.file_name = file_name

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')

# ________________________________________________________
# CBV находятся в модуле gentian_framework.common_views!!!
# ________________________________________________________
