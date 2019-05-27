from unittest import TestCase, main

from expects import expect, be_none, equal

from twin_sister.exceptions import \
    ArgNotSpecified, FunctionNotCalled, KwargNotSpecified
from twin_sister.expects_matchers import complain
from twin_sister.fakes import FunctionSpy


class TestFunctionSpy(TestCase):

    def test_can_specify_return_value(self):
        planted = 42
        spy = FunctionSpy(return_value=planted)
        expect(spy()).to(equal(planted))

    def test_return_value_is_none_if_not_specified(self):
        expect(FunctionSpy()()).to(be_none)

    def test_saves_kwargs_from_first_call(self):
        spy = FunctionSpy()
        planted = {'ooh': 2, 'aah': 4, 'duh': 8}
        spy(**planted)
        spy(foo=1, bar=7, jamf=99)
        args, kwargs = spy.call_history[0]
        expect(kwargs).to(equal(planted))

    def test_saves_kwargs_from_last_call(self):
        spy = FunctionSpy()
        first = {'foo': 1, 'bar': 6, 'baz': 42}
        second = {'spam': 1, 'eggs': 2, 'sausage': 7}
        last = {'larry': 7, 'moe': 12, 'curly': 1}
        spy(**first)
        spy(**second)
        spy(**last)
        args, kwargs = spy.call_history[-1]
        expect(kwargs).to(equal(last))

    def test_saves_args_from_first_call(self):
        spy = FunctionSpy()
        planted = ('groucho', 'harpo', 'chico', 'zeppo')
        spy(*planted)
        spy(1, 2, 3, 4, 5)
        args, kwargs = spy.call_history[0]
        expect(args).to(equal(planted))

    def test_saves_args_from_last_call(self):
        spy = FunctionSpy()
        planted = ('tom', 'ray')
        spy(1, 2, 3)
        spy(*planted)
        args, kwargs = spy.call_history[-1]
        expect(args).to(equal(planted))

    def test_get_numeric_item_returns_arg_from_last_call(self):
        spy = FunctionSpy()
        planted = 'your card'
        spy(1, 23, 44)
        spy(2, planted, 6)
        expect(spy[1]).to(equal(planted))

    def test_get_non_numeric_item_returns_kwarg_from_last_call(self):
        spy = FunctionSpy()
        planted = 'roger'
        spy(1, 22, 44)
        spy(planted=planted)
        expect(spy['planted']).to(equal(planted))

    def test_complains_if_there_were_no_calls(self):
        expect(lambda: FunctionSpy()[0]).to(complain(FunctionNotCalled))

    def test_kwargs_from_last_call_returns_kwargs_from_last_call(self):
        planted = {'do': 1, 're': 2, 'mi': 3}
        spy = FunctionSpy()
        spy(foo=2, bar=7)
        spy(**planted)
        expect(spy.kwargs_from_last_call()).to(equal(planted))

    def test_kwargs_from_last_call_complains_when_there_are_no_calls(self):
        expect(FunctionSpy().kwargs_from_last_call).to(
            complain(FunctionNotCalled))

    def test_args_from_last_call_returns_args_from_last_call(self):
        planted = (5, 4, 1, 27)
        spy = FunctionSpy()
        spy()
        spy(7, 22)
        spy(*planted)
        expect(spy.args_from_last_call()).to(equal(planted))

    def test_args_from_last_call_complains_when_there_are_no_calls(self):
        expect(FunctionSpy().args_from_last_call).to(
            complain(FunctionNotCalled))

    def test_assert_was_called_complains_when_not_called(self):
        spy = FunctionSpy()
        expect(spy.assert_was_called).to(complain(FunctionNotCalled))

    def test_assert_was_called_does_not_complain_when_called(self):
        spy = FunctionSpy()
        spy()
        expect(spy.assert_was_called).not_to(complain(FunctionNotCalled))

    def test_last_call_returns_args_and_kwargs(self):
        planted_args = (1, 7, 2)
        planted_kwargs = {'reply': "I don't like SPAM!"}
        spy = FunctionSpy()
        spy(2, blah=4)
        spy(*planted_args, **planted_kwargs)
        expect(spy.last_call()).to(equal((planted_args, planted_kwargs)))

    def test_last_call_complains_when_not_called(self):
        expect(FunctionSpy().last_call).to(complain(FunctionNotCalled))

    def test_complains_when_requested_kwarg_is_absent(self):
        spy = FunctionSpy()
        spy(things=2)
        expect(lambda: spy['stuff']).to(complain(KwargNotSpecified))

    def test_complains_when_requested_arg_is_absent(self):
        spy = FunctionSpy()
        spy(0, 1)
        expect(lambda: spy[2]).to(complain(ArgNotSpecified))


if '__main__' == __name__:
    main()
