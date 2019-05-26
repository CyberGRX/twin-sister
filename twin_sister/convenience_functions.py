from contextlib import contextmanager

from .injection.dependency_context import DependencyContext
from .injection.dependency_registry import DependencyRegistry


def close_all_dependency_contexts():
    DependencyRegistry.reset()


def dependency(dep):
    context = DependencyRegistry.current_context()
    if context:
        return context.get(dep)
    return dep


@contextmanager
def dependency_context(**kwargs):
    """
    kwargs get passed to DependencyContext initializer
    """
    context = open_dependency_context(**kwargs)
    yield context
    context.close()


def open_dependency_context(**kwargs):
    """
    kwargs get passed to DependencyContext initializer
    """
    context = DependencyContext(**kwargs)
    DependencyRegistry.register(context)
    return context
