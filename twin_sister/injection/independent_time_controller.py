from twin_sister.injection.context_time_controller import ContextTimeController
from twin_sister.injection.dependency_context import DependencyContext


def IndependentTimeController(
        target, *, daemon=True, parent_context=None, **kwargs):

    """
    Facade for the sake of backward compatibility.

    A TimeController that can be initialized without specifying a parent
    context
    """

    return ContextTimeController(
        target=target, daemon=daemon,
        parent_context=parent_context or DependencyContext(),
        **kwargs)
