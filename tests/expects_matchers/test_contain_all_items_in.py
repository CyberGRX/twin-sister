from unittest import TestCase, main

from expects import expect

from twin_sister.expects_matchers import contain_all_items_in


class TestContainAllItemsIn(TestCase):

    def test_false_if_one_item_missing(self):
        expect({'spam': 1, 'eggs': 4}).not_to(
            contain_all_items_in({'spam': 1, 'eggs': 4, 'beans': 7}))

    def test_false_if_one_item_has_unexpected_value(self):
        expect({'spam': 1, 'eggs': 4}).not_to(
            contain_all_items_in({'spam': 1, 'eggs': 5}))

    def test_true_if_exact_match(self):
        things = {'spam': 1, 'eggs': [4, 1], 'beans': 0}
        expect(things).to(contain_all_items_in(things))

    def test_true_if_all_expectations_met_and_extra_items_present(self):
        expect({'spam': 1, 'eggs': 4, 'ximinez': 7}).to(
            contain_all_items_in({'spam': 1, 'eggs': 4}))

    def test_true_if_all_expectations_met_expect_for_ignored_keys(self):
        expect({'spam': 1, 'eggs': 4, 'toast': 5}).to(
            contain_all_items_in({'spam': 1, 'eggs': 4, 'toast': 0},
                                 ignore_keys=['toast']))


if '__main__' == __name__:
    main()
