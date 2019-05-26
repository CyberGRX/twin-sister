from contextlib import contextmanager

from .empty_fake import EmptyFake


@contextmanager
def empty_context_manager(*args, **kwargs):
    yield EmptyFake()
