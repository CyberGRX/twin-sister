from datetime import datetime
from threading import Thread

from twin_sister.fakes import FakeDatetime


class ContextTimeController(Thread):
    """
    Executes a function in a new thread that uses a fake datetime.
    This allows a test to manipulate time as perceived by the target function.
    """

    """Initializer

    Behaves exactly like Thread.__init__ except that daemon defaults to
    True.

    target -- function to call in the thread
    parent_context -- inherit dependencies injected into this context
    """
    def __init__(self, target, *args, parent_context, **kwargs):
        super().__init__(target=target, **kwargs)
        self.exception_caught = None
        self.value_returned = None
        self.fake_datetime = FakeDatetime()
        self._context = parent_context.spawn()
        self._target = target

    """Advance the fake clock by the given interval

    Raises a RuntimeError if the thread has not been started.
    Keyword arguments can be anything accepted by datetime.timedelta.
    """
    def advance(self, **kwargs):
        if not self.ident:
            raise RuntimeError(
                'The thread must be started before advancing time')
        self.fake_datetime.advance(**kwargs)

    def run(self):
        self._context.inject(datetime, self.fake_datetime)
        self._context.attach_to_thread(self)
        try:
            self.value_returned = self._target()
        except Exception as e:
            self.exception_caught = e
