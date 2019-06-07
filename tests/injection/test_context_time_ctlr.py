from datetime import datetime, timedelta
from time import sleep
from unittest import TestCase, main

from expects import expect, be_false, be_true, equal, raise_error

from twin_sister import dependency, dependency_context
from twin_sister.fakes import FakeDatetime
from twin_sister.injection.dependency_context import DependencyContext


class TestContextTimeController(TestCase):

    def test_advance_complains_if_not_started(self):
        with dependency_context() as context:
            sut = context.create_time_controller(target=lambda: None)

            def attempt():
                sut.advance(seconds=1)
            expect(attempt).to(raise_error(RuntimeError))

    def test_advance_advances_time_by_specified_delta(self):
        reported_time = None

        def canary():
            nonlocal reported_time
            while True:
                reported_time = dependency(datetime).now()

        with dependency_context() as context:
            sut = context.create_time_controller(target=canary, daemon=True)
            sut.start()
            sleep(0.05)  # Give SUT a chance to get started
            start_time = sut.fake_datetime.now()
            advance_delta = 42
            sut.advance(seconds=advance_delta)
            sleep(0.05)  # Give SUT a chance to cycle
            expect(reported_time).to(
                equal(start_time + timedelta(seconds=advance_delta)))

    def test_stores_exception(self):
        exception_raised = Exception('intentional')

        def boom():
            raise exception_raised
        with dependency_context() as context:
            sut = context.create_time_controller(target=boom, daemon=True)
            sut.start()
            sut.join()
            expect(sut.exception_caught).to(equal(exception_raised))

    def test_stores_return_value(self):
        expected = 42
        with dependency_context() as context:
            sut = context.create_time_controller(
                target=lambda: expected, daemon=True)
            sut.start()
            sut.join()
            expect(sut.value_returned).to(equal(expected))

    def test_thread_is_daemonic_by_default(self):
        with dependency_context() as context:
            sut = context.create_time_controller(target=print)
        expect(sut.daemon).to(be_true)

    def test_thread_is_not_daemonic_when_default_overridden(self):
        with dependency_context() as context:
            sut = context.create_time_controller(target=print, daemon=False)
            expect(sut.daemon).to(be_false)

    def test_inherits_origin_context(self):
        with dependency_context() as context:
            key = 'dennis'
            value = 37
            context.inject(key, 'something else')
            ctl = context.create_time_controller(
                target=lambda: dependency(key))
            context.inject(key, value)
            ctl.start()
            ctl.join()
            expect(ctl.value_returned).to(equal(value))

    def test_does_not_affect_origin_context(self):
        keep_running = True

        def forrest():
            while keep_running:
                sleep(0.001)

        with dependency_context() as context:
            original_context_time = datetime.fromtimestamp(2)
            context_dt = FakeDatetime(fixed_time=original_context_time)
            context.inject(datetime, context_dt)
            tc = context.create_time_controller(target=forrest)
            tc.start()
            sleep(0.01)
            expect(dependency(datetime).now()).to(equal(original_context_time))
        keep_running = False
        tc.join()

    def test_inherits_arbitrary_key_from_parent_context(self):
        key = object()
        parent_value = 'something'
        child_value = None

        def fetch():
            nonlocal child_value
            child_value = dependency(key)

        parent_context = DependencyContext()
        parent_context.inject(key, parent_value)
        tc = parent_context.create_time_controller(target=fetch)
        tc.start()
        tc.join()
        expect(child_value).to(equal(parent_value))


if '__main__' == __name__:
    main()
