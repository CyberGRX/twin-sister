from unittest import TestCase, main

from expects import expect, equal

from twin_sister.expects_matchers import raise_ex


class Spam(Exception):
    pass


class SonOfSpam(Spam):
    pass


class Eggs(Exception):
    pass


class TestRaiseEx(TestCase):

    def test_returns_true_if_specified_exception_is_raised(self):
        def attempt():
            raise Spam('intentional')
        expect(attempt).to(raise_ex(Spam))

    def test_returns_true_if_subclass_exception_is_raised(self):
        def attempt():
            raise SonOfSpam('intentional')
        expect(attempt).to(raise_ex(Spam))

    def test_returns_false_if_no_exception_is_raised(self):
        expect(lambda: None).not_to(raise_ex(Spam))

    def test_returns_false_if_msg_pat_specified_and_does_not_match(self):
        def attempt():
            raise Spam('Nobody injests the Spinach Imposition')
        expect(attempt).not_to(raise_ex(Spam, '^Spinach'))

    def test_returns_true_if_msg_pat_specified_and_matches(self):
        def attempt():
            raise Spam('Spinach is king')
        expect(attempt).to(raise_ex(Spam, '^Spinach'))

    def test_raises_unspecfied_exception(self):
        raised = Eggs('intentional')

        def attempt():
            raise raised

        caught = None
        try:
            expect(attempt).to(raise_ex(Spam))
        except Exception as e:
            caught = e
        expect(caught).to(equal(raised))

    def test_returns_true_on_exception_object_exact_match(self):
        e = Spam("I'll have your SPAM and your little dog too")

        def attempt():
            raise e

        expect(attempt).to(raise_ex(e))

    def test_re_raises_another_exception_of_same_class(self):
        expected = Spam('expected')
        unexpected = Spam('unexpected')

        def attempt():
            raise unexpected

        try:
            expect(attempt).to(raise_ex(expected))
            assert False, 'No exception was raised'
        except Spam as actual:
            expect(actual).to(equal(unexpected))

    def test_re_raises_another_exception_of_different_class(self):
        expected = Spam('expected')
        unexpected = Eggs('unexpected')

        def attempt():
            raise unexpected

        try:
            expect(attempt).to(raise_ex(expected))
            assert False, 'No exception was raised'
        except type(unexpected) as actual:
            expect(actual).to(equal(unexpected))

    def test_returns_false_if_object__specified_and_nothing_raised(self):
        expect(lambda: None).not_to(raise_ex(Exception('unexpected')))


if '__main__' == __name__:
    main()
