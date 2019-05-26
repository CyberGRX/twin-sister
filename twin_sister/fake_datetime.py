from datetime import datetime, timedelta


class FakeDatetime:
    """Fakes datetime.datetime so we can control time
    """

    def __init__(self):
        self._now = datetime.fromtimestamp(1503083117)

    def advance(self, **kwargs):
        """Advance the fake clock by some time delta

        kwargs -- Anything that can be passed to datetime.timedelta
        """
        self._now = self._now + timedelta(**kwargs)

    # Real interface
    def now(self):
        return self._now

    utcnow = now

    def __call__(self, *args, **kwargs):
        return datetime(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(datetime, name)
