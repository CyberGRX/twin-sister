from unittest import TestCase, main
from unittest.mock import patch

from expects import expect, be_a, be_true, equal
from expects.matchers import Matcher

from twin_sister.expects_matchers import eventually


class TimeoutSentinel:
    def __init__(self, truth_trigger, timeout_trigger):
        self.truth_trigger = truth_trigger
        self.timeout_trigger = timeout_trigger
        self.times_called = 0

    def __call__(self):
        self.times_called += 1
        return self.truth_triggered()

    def truth_triggered(self):
        return self.times_called >= self.truth_trigger

    def timeout_triggered(self):
        return self.times_called >= self.timeout_trigger


class FakeNow:
    def __init__(self, truth_call_trigger, timeout_call_trigger):
        self.sentinel = TimeoutSentinel(truth_call_trigger,
                                        timeout_call_trigger)
        self.timeout_configured = False
        self.added_delta = None

    def __add__(self, other):
        self.added_delta = other
        self.timeout_configured = True
        return other

    def __call__(self):
        return self

    def __lt__(self, other):
        if not self.timeout_configured:
            raise AssertionError(
                'Configure a timeout before checking if timed out.')
        return not self.sentinel.timeout_triggered()


class FakeSleep:
    def __init__(self):
        self.slept_time = None

    def __call__(self, seconds):
        self.slept_time = seconds


class TestEventuallyMatcher(TestCase):
    def setUp(self):
        self.module_path = 'twin_sister.expects_matchers.eventually_matchers'
        self.patcher = patch(f'{self.module_path}.sleep',
                             new_callable=FakeSleep)
        self.fake_sleep = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_eventually_matcher_inherits_from_matcher(self):
        expect(eventually('', timeout=0, throttle=0)).to(be_a(Matcher))

    def test_eventually_matches_when_subject_function_return_matches(self):
        expect(lambda: True).to(
            eventually(be_true, timeout=0, throttle=0))

    def test_eventually_matches_when_function_matches_before_timeout(self):
        with patch(f'{self.module_path}.now',
                   new_callable=FakeNow,
                   truth_call_trigger=2,
                   timeout_call_trigger=3) as fake_now:
            matcher = eventually(be_true, timeout=0, throttle=0)
            match_result = matcher._match(fake_now.sentinel)

            assert match_result[0], \
                'Match returned False when truth condition ' \
                'should have triggered before timeout.'

    def test_eventually_doesnt_match_before_truth_trigger(self):
        with patch(f'{self.module_path}.now',
                   new_callable=FakeNow,
                   truth_call_trigger=2,
                   timeout_call_trigger=3) as fake_now:
            matcher = eventually(be_true, timeout=0, throttle=0)
            matcher._match(fake_now.sentinel)

            assert fake_now.sentinel.truth_triggered(), \
                'Did not meet truth condition before returning a match.'

    def test_eventually_doesnt_match_after_timeout_trigger(self):
        with patch(f'{self.module_path}.now',
                   new_callable=FakeNow,
                   truth_call_trigger=2,
                   timeout_call_trigger=3) as fake_now:
            matcher = eventually(be_true, timeout=0, throttle=0)
            matcher._match(fake_now.sentinel)

            assert not fake_now.sentinel.timeout_triggered(), \
                'Timeout was triggered despite getting a match.'

    def test_eventually_negates_match_if_function_matches_after_timeout(self):
        with patch(f'{self.module_path}.now',
                   new_callable=FakeNow,
                   truth_call_trigger=3,
                   timeout_call_trigger=2) as fake_now:
            matcher = eventually(be_true, timeout=0, throttle=0)
            match_result = matcher._match(fake_now.sentinel)

            assert not match_result[0], \
                'Matcher matched when function never reached truth condition.'

    def test_eventually_doesnt_negate_before_timeout_trigger(self):
        with patch(f'{self.module_path}.now',
                   new_callable=FakeNow,
                   truth_call_trigger=3,
                   timeout_call_trigger=2) as fake_now:
            matcher = eventually(be_true, timeout=0, throttle=0)
            matcher._match(fake_now.sentinel)

            assert fake_now.sentinel.timeout_triggered(), \
                'Match negated without a encountering a timeout trigger.'

    def test_eventually_doesnt_negate_when_truth_condition_not_met(self):
        with patch(f'{self.module_path}.now',
                   new_callable=FakeNow,
                   truth_call_trigger=3,
                   timeout_call_trigger=2) as fake_now:
            matcher = eventually(be_true, timeout=0, throttle=0)
            matcher._match(fake_now.sentinel)

            assert not fake_now.sentinel.truth_triggered(), \
                'Match negated despite encountering the truth condition.'

    def test_eventually_sleeps_with_throttle(self):
        expected_throttle = 5

        with patch(f'{self.module_path}.now',
                   new_callable=FakeNow,
                   truth_call_trigger=2,
                   timeout_call_trigger=3) as fake_now:

            matcher = eventually(be_true, timeout=0, throttle=expected_throttle)
            matcher._match(fake_now.sentinel)

            expect(self.fake_sleep.slept_time).to(equal(expected_throttle))

    def test_eventually_configures_timedelta_with_timeout(self):
        expected_timeout = 5

        class FakeTimedelta:
            def __init__(self):
                self.delta = None

            def __call__(self, *, seconds):
                self.delta = seconds

        with patch(f'{self.module_path}.now',
                   new_callable=FakeNow,
                   truth_call_trigger=2,
                   timeout_call_trigger=3) as fake_now:
            with patch(f'{self.module_path}.timedelta',
                       new_callable=FakeTimedelta) as fake_timedelta:
                matcher = eventually(be_true,
                                     timeout=expected_timeout,
                                     throttle=0)
                matcher._match(fake_now.sentinel)

                expect(fake_timedelta.delta).to(equal(expected_timeout))


if __name__ == "__main__":
    main()
