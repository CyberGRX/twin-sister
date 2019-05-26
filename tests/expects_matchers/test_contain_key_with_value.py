from unittest import TestCase, main

from expects import expect

from twin_sister.expects_matchers import contain_key_with_value


class TestContainsKeyWithValue(TestCase):

    def test_true_if_contains_key_with_value(self):
        expect({'spam': 1, 'eggs': 2}).to(
            contain_key_with_value('eggs', 2))

    def test_false_if_contains_key_with_different_value(self):
        expect({'spam': 1, 'eggs': 2}).not_to(
            contain_key_with_value('eggs', 'the spinach imposition'))

    def test_false_if_does_not_contain_key(self):
        expect({'spam': 1, 'eggs': 2}).not_to(
            contain_key_with_value('beans', 1))


if '__main__' == __name__:
    main()
