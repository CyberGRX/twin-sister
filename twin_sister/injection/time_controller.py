from datetime import datetime
from threading import Thread

from twin_sister.convenience_functions import dependency_context

from .fake_datetime import FakeDatetime


class TimeController(Thread):
    """
    Executes a function in a new thread that uses a fake datetime.
    This allows a test to manipulate time as perceived by the target function.
    """
    def __init__(self, target, *, parent_context=None, **kwargs):
        """Initializer

        Behaves exactly like Thread.__init__ except that daemon defaults to
        True.

        target -- function to call in the thread
        parent_context -- inherit dependencies injected into this context
        """
        self._parent_context = parent_context
        self._target = target
        if 'daemon' not in kwargs.keys():
            kwargs['daemon'] = True
        super().__init__(target=target, **kwargs)
        self.fake_datetime = FakeDatetime()
        self.exception_caught = None
        self.value_returned = None

    def advance(self, **kwargs):
        """Advance the fake clock by the given interval

        Raises a RuntimeError if the thread has not been started.
        Keyword arguments can be anything accepted by datetime.timedelta.
        """
        if not self.ident:
            raise RuntimeError(
                'The thread must be started before advancing time')
        self.fake_datetime.advance(**kwargs)

    def run(self):
        with dependency_context(parent=self._parent_context) as context:
            context.inject(datetime, self.fake_datetime)
            context.attach_to_thread(self)
            try:
                self.value_returned = self._target()
            except Exception as e:
                self.exception_caught = e
