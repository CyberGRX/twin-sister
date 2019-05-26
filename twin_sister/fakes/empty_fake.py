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

    def __getattr__(self, name):
        return self.__spawn()

    def __getitem__(self, key):
        return self.__spawn()

    __ge__ = __eq__

    def __gt__(self, other):
        return False

    def __hash__(self):
        return self.__hash

    def __init__(self, *args, **kwargs):
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
