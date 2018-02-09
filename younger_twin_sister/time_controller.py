from datetime import datetime
from threading import Thread

from .convenience_functions import dependency_context
from .fake_datetime import FakeDatetime


class TimeController(Thread):
    """
    Executes a function in a new thread that uses a fake datetime.
    This allows a test to manipulate time as perceived by the target function.
    """
    def __init__(self, **kwargs):
        """Initializer

        Behaves exactly like Thread.__init__ except that daemon defaults to
        True.
        """
        self._target = kwargs['target']
        if 'daemon' not in kwargs.keys():
            kwargs['daemon'] = True
        super().__init__(**kwargs)
        self.fake_datetime = FakeDatetime()
        self.exception_caught = None

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
        with dependency_context() as context:
            context.inject(datetime, self.fake_datetime)
            context.attach_to_thread(self)
            try:
                self._target()
            except Exception as e:
                self.exception_caught = e
