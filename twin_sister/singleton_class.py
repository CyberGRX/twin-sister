class SingletonClass:
    """
    "class" which returns the same instance very time it is invoked
    """

    def __init__(self, instance):
        self.instance = instance

    def __call__(self, *args, **kwargs):
        return self.instance

    def __getattr__(self, name):
        return getattr(self.instance.__class__, name)
