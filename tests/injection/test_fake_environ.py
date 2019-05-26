import os
from unittest import TestCase, main

from expects import expect, be, equal

from twin_sister import dependency, dependency_context
from twin_sister.injection.dependency_context import DependencyContext


class TestFakeEnviron(TestCase):

    def test_supplies_empty_environment_if_set(self):
        with dependency_context(supply_env=True):
            expect(dependency(os).environ).to(equal({}))

    def test_does_not_affect_other_os_attributes(self):
        with dependency_context(supply_env=True):
            expect(dependency(os).getpid).to(be(os.getpid))

    def test_also_initially_empty_with_fake_fs(self):
        with dependency_context(supply_env=True, supply_fs=True):
            expect(dependency(os).environ).to(equal({}))

    def test_plays_nicely_with_fake_fs(self):
        key = 'something_i_made_up'
        value = 'Playdoh(tm)'
        with dependency_context(supply_env=True, supply_fs=True) as context:
            context.os.environ[key] = value
            expect(dependency(os).environ[key]).to(equal(value))

    def test_supplies_real_environment_if_unset(self):
        with dependency_context():
            expect(dependency(os).environ).to(equal(os.environ))

    def test_incompatible_with_specifified_parent_context(self):
        try:
            DependencyContext(
                parent=DependencyContext(), supply_env=True)
            assert False, 'No exception was raised'
        except ValueError:
            pass

    def test_inherits_parent_context_os(self):
        parent = DependencyContext(supply_env=True)
        with dependency_context(parent=parent):
            expect(dependency(os)).to(be(parent.os))


if '__main__' == __name__:
    main()
