from time import time


class AppRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


def route(routes, url):
    def wrapper(cls):
        routes[url] = cls()
    return wrapper


class Debug:
    def __call__(self, method):
        def timed(obj, *args, **kw):
            ts = time()
            result = method(obj, *args, **kw)
            te = time()
            delta = te - ts
            print(f'debug --> {obj.__class__.__name__} выполнялся {delta:2.2f} ms')
            return result
        return timed


def debug(method):
    def wrapper(self, *args, **kw):
        ts = time()
        result = method(self, *args, **kw)
        te = time()
        delta = te - ts
        print(f'debug --> {self.__class__.__name__} выполнялся {delta:2.2f} ms')
        return result
    return wrapper
