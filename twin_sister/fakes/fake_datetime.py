from datetime import datetime, timedelta


class FakeDatetime:
    """
    Partially fakes datetime.datetime
    """

    def __init__(self, fixed_time=None):
        self.fixed_time = fixed_time or datetime.fromtimestamp(1503083117)

    def advance(self, **kwargs):
        """Advance the fake clock by some time delta

        kwargs -- Anything that can be passed to datetime.timedelta
        """
        self.fixed_time += timedelta(**kwargs)

    def now(self):
        return self.fixed_time

    utcnow = now

    __call__ = datetime

    def __getattr__(self, name):
        return getattr(datetime, name)
