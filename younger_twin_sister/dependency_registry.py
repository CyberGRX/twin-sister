from threading import get_ident as get_thread_id


class DependencyRegistry:

    @classmethod
    def current_context(cls):
        thread_id = get_thread_id()
        if thread_id in cls._context_stacks:
            stack = cls._context_stacks[thread_id]
            if stack:
                return stack[-1]
        return None

    @classmethod
    def register(cls, context, *, thread_id=None):
        if thread_id is None:
            thread_id = get_thread_id()
        if thread_id not in cls._context_stacks:
            cls._context_stacks[thread_id] = []
        cls._context_stacks[thread_id].append(context)

    @classmethod
    def reset(cls):
        # thread_id -> stack of DependencyContext objects
        cls._context_stacks = {}

    @classmethod
    def unregister(cls, context, *, thread_id=None):
        if thread_id is None:
            thread_id = get_thread_id()
        try:
            cls._context_stacks[thread_id].remove(context)
        except KeyError:
            # Sometimes, cleanup can fail due to a race condition
            # If it's gone, it's gone.  No need to raise an exception.
            pass


DependencyRegistry.reset()
