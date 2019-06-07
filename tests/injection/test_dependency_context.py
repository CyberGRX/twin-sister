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

    def test_spawned_context_returns_value_from_parent(self):
        key = object()
        parent_value = 46
        parent = DependencyContext()
        parent.inject(key, parent_value)
        child = parent.spawn()
        expect(child.get(key)).to(be(parent_value))

    def test_spawned_context_can_override_parent_value(self):
        key = object()
        parent_value = 37
        child_value = 2
        parent = DependencyContext()
        parent.inject(key, parent_value)
        child = parent.spawn()
        child.inject(key, child_value)
        expect(child.get(key)).to(be(child_value))

    def test_spawned_context_does_not_replace_parent_value(self):
        key = object()
        parent_value = 37
        child_value = 2
        parent = DependencyContext()
        parent.inject(key, parent_value)
        child = parent.spawn()
        child.inject(key, child_value)
        expect(parent.get(key)).to(be(parent_value))


if '__main__' == __name__:
    main()
