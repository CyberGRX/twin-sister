from .dependency_registry import DependencyRegistry
from .fake_singleton import FakeSingleton
from .singleton_class import SingletonClass


class DependencyContext:

    def __init__(self):
        self._injected = {}

    def close(self):
        DependencyRegistry.unregister(self)

    def get(self, dependency):
        if dependency in self._injected:
            return self._injected[dependency]
        else:
            return dependency

    def inject(self, dependency, injected):
        self._injected[dependency] = injected

    def inject_as_class(self, dependency, injected):
        """
        Inject an object as though it were a class.
        When the victim requests the class, the injector returns
        a SingletonClass which wraps the injected object.
        """
        self.inject(dependency, SingletonClass(injected))

    def inject_as_singleton(self, dependency, injected):
        """
        Inject as an object as though it were a singleton.
        When the victim requests the class, the injector returns an object
        with an "instance" method which returns the injected object.
        """
        self.inject(dependency, FakeSingleton(injected))
