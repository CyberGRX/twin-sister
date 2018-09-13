import os
from unittest import TestCase, main

from expects import expect, be, equal

from younger_twin_sister import dependency, dependency_context


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


if '__main__' == __name__:
    main()
