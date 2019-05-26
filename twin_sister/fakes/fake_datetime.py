from datetime import datetime


class FakeDatetime:
    """
    Partially fakes datetime.datetime
    """

    def __init__(self, fixed_time=None):
        self.fixed_time = fixed_time or datetime.now()

    def now(self):
        return self.fixed_time

    utcnow = now

    def __getattr__(self, name):
        return getattr(datetime, name)
