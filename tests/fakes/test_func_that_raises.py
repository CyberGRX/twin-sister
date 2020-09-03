from unittest import TestCase, main

from expects import expect
from twin_sister.expects_matchers import raise_ex
from twin_sister.fakes import func_that_raises


class FakeException(RuntimeError):
    pass


class TestExceptionFunc(TestCase):
    def test_returned_func_raises_expected_exception(self):

        expected = RuntimeError("Shuzbut")
        expect(func_that_raises(expected)).to(raise_ex(expected))

    def test_returned_func_accepts_arbitrary_args(self):
        func = func_that_raises(FakeException())
        try:
            func(1, 2, 3, 4, 5)
            assert False, "No exception was raised"
        except FakeException:
            pass

    def test_returned_func_accepts_arbitrary_kwargs(self):
        func = func_that_raises(FakeException())
        try:
            func(a=1, b=2, c="the spinach inquisition")
            assert False, "No exception was raised"
        except FakeException:
            pass


if "__main__" == __name__:
    main()
