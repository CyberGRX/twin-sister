class Passthrough:

    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        return getattr(self._target, name)
