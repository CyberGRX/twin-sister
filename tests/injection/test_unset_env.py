import os
from unittest import TestCase, main

from expects import expect, equal

from twin_sister.injection.dependency_context import DependencyContext


class TestUnsetEnv(TestCase):

    def test_deletes_specified_entry_only(self):
        context = DependencyContext(supply_env=True)
        context.os.environ = {'spam': 1, 'eggs': 2, 'sausage': 3}
        context.unset_env('eggs')
        expect(context.os.environ).to(equal(
            {'spam': 1, 'sausage': 3}))

    def test_complains_if_env_not_supplied(self):
        key = 'rubbish-set-by-test-unset-env'
        os.environ[key] = 'rubbish'
        context = DependencyContext()
        try:
            context.unset_env(key)
            assert False, 'Caught nothing'
        except RuntimeError:
            pass


if '__main__' == __name__:
    main()
