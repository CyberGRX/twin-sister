import inspect
from random import randrange
import sys


class EmptyFake:
    """
    Object that can serve as a double for almost anything
    """

    @classmethod
    def __spawn(cls):
        return cls()

    def __call__(self, *args, **kwargs):
        return self.__spawn()

    def __contains__(self, item):
        return False

    def __enter__(self):
        return self.__spawn()

    def __exit__(self, *args, **kwargs):
        pass

    def __delitem__(self, key):
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __float__(self):
        return 0.0

    def __pattern_cls_declares(self, name):
        return name in [a for a, _ in inspect.getmembers(self.__pattern_cls)]

    def __getattr__(self, name):
        if self.__pattern_cls and not self.__pattern_cls_declares(name):
            raise AttributeError(
                f'{self.__pattern_cls} does not declare "{name}"')
        if not (
                self.__pattern_obj is None or
                hasattr(self.__pattern_obj, name)):
            raise AttributeError(
                f'{self.__pattern_obj} has no attribute "{name}"')
        return self.__spawn()

    def __getitem__(self, key):
        return self.__spawn()

    __ge__ = __eq__

    def __gt__(self, other):
        return False

    def __hash__(self):
        return self.__hash

    def __init__(self, *args, pattern_cls=None, pattern_obj=None, **kwargs):
        if not (pattern_cls is None or pattern_obj is None):
            raise TypeError(
                'pattern_cls and pattern_obj are mutually exclusive')
        self.__pattern_cls = pattern_cls
        self.__pattern_obj = pattern_obj
        self.__hash = randrange(sys.maxsize-1)

    def __int__(self):
        return 0

    def __iter__(self):
        return self

    __le__ = __eq__

    def __lt__(self, other):
        return False

    def __len__(self):
        return 0

    def __ne__(self, other):
        return not(self == other)

    def __next__(self):
        raise StopIteration()

    def __reversed__(self):
        return self

    def __setitem__(self, key, value):
        pass

    def __str__(self):
        return "(EmptyFake object)"
