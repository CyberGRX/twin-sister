from unittest import TestCase, main

from expects import expect, be

from twin_sister import dependency, dependency_context


class Thing:
    pass


class TestInjectAsSingleton(TestCase):

    def test_as_class(self):
        injected = object()
        with dependency_context() as context:
            context.inject_as_singleton(Thing, injected)
            retrieved = dependency(Thing).instance()
            expect(retrieved).to(be(injected))


if '__main__' == __name__:
    main()
