from datetime import datetime
from unittest import TestCase, main

from expects import expect, be_a, equal

from twin_sister.fakes import FakeDatetime


class TestFakeDatetime(TestCase):

    def test_sets_fixed_time_if_none_specified(self):
        expect(FakeDatetime().fixed_time).to(be_a(datetime))

    def test_can_specify_fixed_time(self):
        now = datetime.now()
        expect(FakeDatetime(fixed_time=now).fixed_time).to(
            equal(now))

    def test_now_returns_fixed_time(self):
        now = datetime.now()
        expect(FakeDatetime(fixed_time=now).now()).to(equal(now))

    def test_utcnow_returns_fixed_time(self):
        now = datetime.now()
        expect(FakeDatetime(fixed_time=now).utcnow()).to(equal(now))

    def test_passes_other_dt_attributes_through(self):
        fake = FakeDatetime()
        for attr in dir(datetime):
            if not(attr.startswith('_') or attr in ('now', 'utcnow')):
                assert getattr(fake, attr) == getattr(datetime, attr), \
                    f'{attr} did not pass through'


if '__main__' == __name__:
    main()
