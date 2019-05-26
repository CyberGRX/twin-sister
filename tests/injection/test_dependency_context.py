from unittest import TestCase, main

from expects import expect, be

from twin_sister.injection.dependency_context import DependencyContext


class TestDependencyContext(TestCase):

    def test_get_returns_original_if_nothing_injected(self):
        sut = DependencyContext()
        expected = object()
        expect(sut.get(expected)).to(be(expected))

    def test_get_returns_original_if_unrelated_injected(self):
        expected = object()
        unrelated = object()
        injected = object()
        sut = DependencyContext()
        sut.inject(unrelated, injected)
        expect(sut.get(expected)).to(be(expected))

    def test_get_returns_injected(self):
        dependency = object()
        injected = object()
        sut = DependencyContext()
        sut.inject(dependency, injected)
        expect(sut.get(dependency)).to(be(injected))


if '__main__' == __name__:
    main()
