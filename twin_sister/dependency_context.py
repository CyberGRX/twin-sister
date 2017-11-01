from .dependency_registry import DependencyRegistry
from .fake_singleton import FakeSingleton
from .singleton_class import SingletonClass


class DependencyContext:

    def __init__(self):
        self._attached_threads = []
        self._injected = {}

    def attach_to_thread(self, thread_object):
        """
        Attach this context to a thread.
        After attachment, calls to "dependency" inside the thread
          will use this context.

        thread_object -- (Thread) Attach to this thread
        """
        thread_id = thread_object.ident
        if not thread_id:
            raise RuntimeError('A running thread is required.')
        DependencyRegistry.register(
            context=self, thread_id=thread_id)
        self._attached_threads.append(thread_id)

    def close(self):
        for t in self._attached_threads:
            DependencyRegistry.unregister(self, thread_id=t)
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
