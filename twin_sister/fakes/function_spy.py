from twin_sister.exceptions import \
    ArgNotSpecified, FunctionNotCalled, KwargNotSpecified


class FunctionSpy:

    def __init__(self, return_value=None):
        self._return_value = return_value
        self.call_history = []

    def assert_was_called(self):
        if not self.call_history:
            raise FunctionNotCalled('The function was not called')

    def last_call(self):
        self.assert_was_called()
        return self.call_history[-1]

    def args_from_last_call(self):
        args, kwargs = self.last_call()
        return args

    def kwargs_from_last_call(self):
        args, kwargs = self.last_call()
        return kwargs

    def __call__(self, *args, **kwargs):
        self.call_history.append((args, kwargs))
        return self._return_value

    def __getitem__(self, item):
        args, kwargs = self.last_call()
        if isinstance(item, int):
            if len(args)-1 < item:
                raise ArgNotSpecified(
                    f'Expected at least {item+1} positional arguments.  '
                    f'Found {args}.')
            return args[item]
        if item not in kwargs.keys():
            raise KwargNotSpecified(
                f'Expected {item} in {set(kwargs.keys())}')
        return kwargs[item]
