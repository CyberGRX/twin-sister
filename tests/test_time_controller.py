from datetime import datetime, timedelta
from time import sleep
from unittest import TestCase, main

from expects import expect, be_false, be_true, equal, raise_error

from twin_sister import TimeController, dependency


class TestTimeController(TestCase):

    def test_advance_complains_if_not_started(self):
        sut = TimeController(target=lambda: None)

        def attempt():
            sut.advance(seconds=1)
        expect(attempt).to(raise_error(RuntimeError))

    def test_advance_advances_time_by_specified_delta(self):
        reported_time = None

        def canary():
            nonlocal reported_time
            while True:
                reported_time = dependency(datetime).now()

        sut = TimeController(target=canary, daemon=True)
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
        sut = TimeController(target=boom, daemon=True)
        sut.start()
        sut.join()
        expect(sut.exception_caught).to(equal(exception_raised))

    def test_stores_return_value(self):
        expected = 42
        sut = TimeController(target=lambda: expected, daemon=True)
        sut.start()
        sut.join()
        expect(sut.value_returned).to(equal(expected))

    def test_thread_is_daemonic_by_default(self):
        sut = TimeController(target=print)
        expect(sut.daemon).to(be_true)

    def test_thread_is_not_daemonic_when_default_overridden(self):
        sut = TimeController(target=print, daemon=False)
        expect(sut.daemon).to(be_false)


if '__main__' == __name__:
    main()
