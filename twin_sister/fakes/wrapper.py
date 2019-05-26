class Wrapper:
    """
    Wraps an object and pretends to be it.
    Can be modified/extended without affecting the underlying object.
    """

    def __init__(self, target, *, affect_only_functions=True):
        self._target = target

    def __bool__(self):
        return bool(self._target)

    def __call__(self, *args, **kwargs):
        return self._target(*args, **kwargs)

    def __dir__(self):
        return dir(self._target)

    def __eq__(self, other):
        return other == self._target

    def __enter__(self):
        return self._target.__enter__()

    def __exit__(self, *args, **kwargs):
        return self._target.__exit__(*args, **kwargs)

    def __float__(self):
        return float(self._target)

    def __getattr__(self, name):
        return getattr(self._target, name)

    def __ge__(self, other):
        return self._target >= other

    def __getitem__(self, key):
        return self._target[key]

    def __gt__(self, other):
        return self._target > other

    def __hash__(self):
        return hash(self._target)

    def __int__(self):
        return int(self._target)

    def __instancecheck__(self, instance):
        return isinstance(self._target, instance)

    def __iter__(self):
        return iter([self.__class__(thing) for thing in self._target])

    def __le__(self, other):
        return self._target <= other

    def __len__(self):
        return len(self._target)

    def __lt__(self, other):
        return self._target < other

    def __ne__(self, other):
        return other != self._target

    def __next__(self):
        return next(self._target)

    def __str__(self):
        return str(self._target)

    def __subclasscheck__(self, subclass):
        return issubclass(self._target, subclass)
