from twin_sister.exceptions import FunctionNotCalled

from .empty_fake import EmptyFake
from .wrapper import Wrapper


def is_a_function(thing):
    return '__call__' in dir(thing)


class MasterSpy(Wrapper):
    """
    Monitors activity on an object.
    Attaches more spies to anything the object returns.
    """

    def __init__(self, target=None, *, affect_only_functions=True):
        if target is None:
            target = EmptyFake()
        super().__init__(target=target)
        self._wrap_non_functions = not affect_only_functions
        self.call_history = []  # [(args, kwargs), (args, kwargs)...]
        self.attribute_spies = {}  # attribute name -> spy
        self.return_value_spies = []

    def __spawn(self, target):
        return(self.__class__(
            target=target,
            affect_only_functions=not self._wrap_non_functions))

    def attribute_was_requested(self, name):
        return name in self.attribute_spies.keys()

    def last_call_to(self, method_name):
        try:
            spy = self.attribute_spies[method_name]
            return spy.call_history[-1]
        except KeyError as e:
            raise FunctionNotCalled('"%s" was not called.' % method_name) from e

    def unwrap_spy_target(self):
        return self._target

    def __call__(self, *args, **kwargs):
        self.call_history.append((args, kwargs))
        return_value = self._target(*args, **kwargs)
        if self._wrap_non_functions or is_a_function(return_value):
            spy = self.__spawn(return_value)
            self.return_value_spies.append(spy)
            return spy
        else:
            return return_value

    def __getattr__(self, name):
        if name in self.attribute_spies.keys():
            val = self.attribute_spies[name]
        else:
            attr = getattr(self._target, name)
            if self._wrap_non_functions or is_a_function(attr):
                spy = self.__spawn(attr)
                self.attribute_spies[name] = spy
                val = spy
            else:
                val = attr
        return val
