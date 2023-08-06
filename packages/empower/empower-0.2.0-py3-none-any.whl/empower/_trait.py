import inspect
from abc import ABCMeta
from functools import wraps


class Trait(metaclass=ABCMeta):
    __trait_modules_used__ = set()


def has_trait(cls, trait_or_tuple):
    return issubclass(cls, trait_or_tuple)


def add_trait_modules_used(trait, module):
    trait.__trait_modules_used__ |= set([module])


def remove_trait_modules_used(trait, module):
    trait.__trait_modules_used__ -= set([module])


class CallerProxy(object):
    def __init__(self, trait, method):
        self.trait = trait

        if isinstance(method, staticmethod):
            self.method = method.__func__
            self.method_type = "staticmethod"
        elif isinstance(method, classmethod):
            self.method = method.__func__
            self.method_type = "classmethod"
        else:
            self.method = method
            self.method_type = "method"

    def __get__(self, obj, T):
        frame = inspect.stack()[1]
        called_module = inspect.getmodule(frame[0])
        if called_module is None:
            module_name = "__main__"
        else:
            module_name = called_module.__name__

        if module_name not in self.trait.__trait_modules_used__:
            raise AttributeError(f"{T} can not call {self.method}")

        @wraps(self.method)
        def wrapper(*args, **kwargs):
            if self.method_type == "staticmethod":
                return self.method(*args, **kwargs)
            elif self.method_type == "classmethod":
                args = [T, *args]
                return self.method(*args, **kwargs)
            else:
                # method
                return self.method(obj, *args, **kwargs)

        return wrapper
