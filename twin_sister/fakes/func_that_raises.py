def func_that_raises(exception):
    """
    Return a function that raises the given exception
    """

    def func(*args, **kwargs):
        raise exception

    return func
