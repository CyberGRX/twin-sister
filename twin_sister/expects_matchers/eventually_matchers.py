import time
import datetime
from expects.matchers import Matcher


def now():
    return datetime.datetime.now()


def sleep(seconds):
    return time.sleep(seconds)


def timedelta(*, seconds):
    return datetime.timedelta(seconds=seconds)


class eventually(Matcher):
    def __init__(self, expected, *, timeout, throttle):
        self._expected = expected
        self._throttle = throttle
        self._timeout = timeout

    def _match(self, subject):
        expiry = now() + timedelta(seconds=self._timeout)
        subject_result = subject()
        match = self._expected._match(subject_result)
        if match[0]:
            return match

        while now() < expiry:
            sleep(self._throttle)
            subject_result = subject()
            match = self._expected._match(subject_result)
            if match[0]:
                return match
        return False, [f'It still returned {subject_result} after '
                       f'{self._timeout} seconds.'] + match[1]

