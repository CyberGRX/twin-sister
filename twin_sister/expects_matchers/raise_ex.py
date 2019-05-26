import re

from expects.matchers import Matcher


class raise_ex(Matcher):
    """
    Similar to the built-in raise_error, but raises unspecified exceptions
    instead of swallowing them.

    exception_or_class -- Return true if this exception
        or an exception with this class is raised
    msg_pattern -- (str) If specified, return false unless the exception
        message matches this pattern
    """

    def __init__(self, exception_or_class, msg_pattern=None):
        self._expected = exception_or_class
        if isinstance(exception_or_class, type):
            self._match = self._match_class
        else:
            self._match = self._match_object
        self._pat = re.compile(msg_pattern) if msg_pattern else None

    def _match_class(self, func):
        caught = None
        try:
            func()
        except self._expected as e:
            caught = e
        if caught is None:
            outcome = False
            msg = 'No exception was raised.'
        elif self._pat is None:
            outcome = True
            msg = 'Caught (%s) %s' % (type(caught), caught)
        elif self._pat.search(str(caught)):
            outcome = True
            msg = 'Caught (%s) %s which matches pattern "%s"' % (
                type(caught), caught, self._pat.pattern)
        else:
            outcome = False
            msg = 'Caught (%s) %s which does not match pattern "%s"' % (
                type(caught), caught, self._pat.pattern)
        return outcome, [msg]

    def _match_object(self, func):
        try:
            func()
        except Exception as caught:
            if caught == self._expected:
                return True, ['Caught the specified exception']
            raise
        return False, ['Nothing was raised']
