from datetime import datetime, timedelta
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

    def test_can_advance_by_arbitrary_ms(self):
        fake = FakeDatetime()
        ms = 235
        start = fake.now()
        fake.advance(milliseconds=ms)
        expect(fake.now()).to(equal(start + timedelta(milliseconds=ms)))

    def test_can_advance_by_arbitrary_sec(self):
        fake = FakeDatetime()
        sec = 235
        start = fake.now()
        fake.advance(seconds=sec)
        expect(fake.now()).to(equal(start + timedelta(seconds=sec)))

    def test_can_advance_by_arbitrary_minutes(self):
        fake = FakeDatetime()
        mins = 4
        start = fake.now()
        fake.advance(minutes=mins)
        expect(fake.now()).to(equal(start + timedelta(minutes=mins)))

    def test_can_advance_by_arbitrary_hours(self):
        fake = FakeDatetime()
        hours = 23
        start = fake.now()
        fake.advance(hours=hours)
        expect(fake.now()).to(equal(start + timedelta(hours=hours)))

    def test_can_advance_by_arbitrary_days(self):
        fake = FakeDatetime()
        days = 8
        start = fake.now()
        fake.advance(days=days)
        expect(fake.now()).to(equal(start + timedelta(days=days)))

    def test_delegates_calls_to_datetime(self):
        expect(FakeDatetime().__call__).to(equal(datetime))


if '__main__' == __name__:
    main()
