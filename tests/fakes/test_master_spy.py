from unittest import TestCase, main

from expects import expect, be, be_a, contain, equal

from twin_sister.exceptions import FunctionNotCalled
from twin_sister.expects_matchers import complain
from twin_sister.fakes import EmptyFake, MasterSpy


class TestMasterSpy(TestCase):

    def test_wraps_empty_fake_if_no_target_supplied(self):
        expect(MasterSpy().unwrap_spy_target()).to(be_a(EmptyFake))

    def test_wraps_target_if_one_supplied(self):
        thing = object()
        expect(MasterSpy(thing).unwrap_spy_target()).to(be(thing))

    def test_does_not_wrap_non_functions_by_default(self):
        target = EmptyFake()
        target.non_func = 42
        spy = MasterSpy(target)
        expect(spy.non_func).to(be(target.non_func))

    def test_can_wrap_non_functions(self):
        target = EmptyFake()
        target.non_func = 42
        spy = MasterSpy(target, affect_only_functions=False)
        expect(spy.non_func).to(be_a(MasterSpy))

    def test_saves_first_function_call(self):
        planted_args = (1, 4, 5)
        planted_kwargs = {'spam': 32, 'eggs': object()}
        stub = EmptyFake()
        stub.func = lambda *a, **k: None
        spy = MasterSpy(stub)
        spy.func(*planted_args, **planted_kwargs)
        spy.func(5, 7, 2, bruces=4, michaels=1)
        expect(spy.attribute_spies['func'].call_history[0]).to(
            equal((planted_args, planted_kwargs)))

    def test_saves_last_function_call(self):
        planted_args = (1, 4, 5)
        planted_kwargs = {'spam': 32, 'eggs': object()}
        stub = EmptyFake()
        stub.func = lambda *a, **k: None
        spy = MasterSpy(stub)
        spy.func(5, 7, 2, bruces=4, michaels=1)
        spy.func()
        spy.func(*planted_args, **planted_kwargs)
        expect(spy.attribute_spies['func'].call_history[-1]).to(
            equal((planted_args, planted_kwargs)))

    def test_saves_first_return_value(self):
        values = range(3)
        it = iter(values)

        def func():
            return next(it)

        spy = MasterSpy(func, affect_only_functions=False)
        for i in values:
            spy()
        expect(spy.return_value_spies[0].unwrap_spy_target()).to(
            equal(values[0]))

    def test_saves_last_return_value(self):
        values = range(3)
        it = iter(range(3))

        def func():
            return next(it)

        spy = MasterSpy(func, affect_only_functions=False)
        for i in values:
            spy()
        expect(spy.return_value_spies[-1].unwrap_spy_target()).to(
            equal(values[-1]))

    def test_applies_affect_only_functions_flag_recursively(self):
        child = EmptyFake()
        child.value = 7
        parent = EmptyFake()
        parent.get_child = lambda: child
        parent_spy = MasterSpy(parent, affect_only_functions=False)
        parent_spy.get_child()
        func_spy = parent_spy.attribute_spies['get_child']
        ret_spy = func_spy.return_value_spies[0]
        ret_spy.value
        expect(ret_spy.attribute_spies.keys()).to(
            contain('value'))

    def test_call_returns_return_value(self):
        value = 27
        spy = MasterSpy(lambda: value)
        expect(spy()).to(equal(value))

    def test_last_call_to_returns_last_call_to_given_func(self):
        stub = EmptyFake()
        stub.func = lambda *a, **k: None
        spy = MasterSpy(stub)
        planted_args = (4, 5)
        planted_kwargs = {'foo': 77, 'bar': 'soap'}
        spy.func(spam=1, eggs=2)
        spy.func(*planted_args, **planted_kwargs)
        expect(spy.last_call_to('func')).to(
            equal((planted_args, planted_kwargs)))

    def test_last_call_to_raises_function_not_called(self):
        stub = EmptyFake()
        stub.func = lambda: None
        spy = MasterSpy(stub)
        expect(lambda: spy.last_call_to('func')).to(
            complain(FunctionNotCalled))

    def test_attribute_requested_returns_true_if_tracking_and_requested(self):
        stub = EmptyFake()
        stub.thing = None
        spy = MasterSpy(stub, affect_only_functions=False)
        spy.thing
        assert spy.attribute_was_requested('thing'), \
            'Spy did not report that attribute was requested'

    def test_getattr_returns_requested_attribute(self):
        stub = EmptyFake()
        stub.thing = 42
        spy = MasterSpy(stub)
        expect(spy.thing).to(equal(stub.thing))

    def test_attribute_requested_returns_false_if_tracking_and_not_req(self):
        stub = EmptyFake()
        stub.thing = None
        spy = MasterSpy(stub, affect_only_functions=False)
        assert not spy.attribute_was_requested('thing'), \
            'Spy reported that attribute was requested'

    def test_unwrapp_spy_target_returns_unwrapped_target(self):
        target = 7
        expect(MasterSpy(target).unwrap_spy_target()).to(
            be(target))


if '__main__' == __name__:
    main()
