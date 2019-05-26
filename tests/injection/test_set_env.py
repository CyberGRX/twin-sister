from unittest import TestCase, main

from expects import expect, equal

from twin_sister.injection.dependency_context import DependencyContext


class TestSetEnv(TestCase):

    def test_can_set_arbitrary_var(self):
        key = 'some_key'
        value = 'some_value'
        context = DependencyContext(supply_env=True)
        context.set_env(**{key: value})
        expect(context.os.environ[key]).to(equal(value))

    def test_can_set_multiple_vars(self):
        k1 = 'doe'
        v1 = 'a deer, a female deer'
        k2 = 'ray'
        v2 = 'a drop of golden sun'
        context = DependencyContext(supply_env=True)
        context.set_env(**{k1: v1, k2: v2})
        expect(context.os.environ[k1]).to(equal(v1))
        expect(context.os.environ[k2]).to(equal(v2))

    def test_can_replace_existing_var(self):
        key = 'quokka'
        old = 'old value'
        new = 'new value'
        context = DependencyContext(supply_env=True)
        context.set_env(**{key: old})
        context.set_env(**{key: new})
        expect(context.os.environ[key]).to(equal(new))

    def test_does_not_affect_unspecified_var(self):
        existing_key = 'dog_milk'
        existing_value = 'Lasts longer than any other milk'
        context = DependencyContext(supply_env=True)
        context.os.environ[existing_key] = existing_value
        context.set_env(goat_milk='and little lambs eat ivy')
        expect(context.os.environ[existing_key]).to(
            equal(existing_value))

    def test_converts_number_to_string(self):
        context = DependencyContext(supply_env=True)
        context.set_env(n=13)
        expect(context.os.environ['n']).to(equal(str(13)))

    def test_converts_bool_to_string(self):
        context = DependencyContext(supply_env=True)
        context.set_env(n=False)
        expect(context.os.environ['n']).to(equal(str(False)))

    def test_converts_arbitrary_rubbish_to_string(self):
        context = DependencyContext(supply_env=True)
        rubbish = {'menu': ['spam', 'eggs', 'sausage', 'biggles']}
        context.set_env(rubbish=rubbish)
        expect(context.os.environ['rubbish']).to(
            equal(str(rubbish)))

    def test_complains_if_env_not_supplied(self):
        context = DependencyContext()
        try:
            context.set_env(things='0')
            assert False, 'No exception was raised'
        except RuntimeError:
            pass


if '__main__' == __name__:
    main()
