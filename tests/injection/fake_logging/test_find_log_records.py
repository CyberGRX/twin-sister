import logging
from unittest import TestCase, main

from expects import expect, be_empty, equal

from twin_sister.fakes import EndlessFake
from twin_sister.injection.fake_logging import FakeLogging


def log_record(level, msg):
    return logging.LogRecord(
        name="spam", level=level, pathname="spam", lineno=1, msg=msg, args={}, exc_info=EndlessFake()
    )


class TestFindLogRecords(TestCase):
    def test_finds_partial_text_on_partial_match(self):
        level = logging.INFO
        log = FakeLogging()
        log.stored_records = [
            log_record(level=level, msg="There's some lovely filth down here!"),
            log_record(level=level, msg="heehaw"),
        ]
        expect(log.find_log_records(level=level, partial_text="lovely filth")).to(equal([log.stored_records[0]]))

    def test_finds_partial_text_on_full_match(self):
        level = logging.INFO
        log = FakeLogging()
        msg = "I don't know much about art but I know what I like"
        log.stored_records = [
            log_record(level=level, msg="There's some lovely filth down here!"),
            log_record(level=level, msg=msg),
        ]
        expect(log.find_log_records(level=level, partial_text=msg)).to(equal([log.stored_records[1]]))

    def test_returns_empty_when_no_text_matches(self):
        level = logging.INFO
        log = FakeLogging()
        log.stored_records = [
            log_record(level=level, msg="There's some lovely filth down here!"),
            log_record(level=level, msg="heehaw"),
        ]
        expect(log.find_log_records(level=level, partial_text="lovely spam")).to(be_empty)

    def test_finds_multiple_matches(self):
        level = logging.INFO
        log = FakeLogging()
        log.stored_records = [
            log_record(level=level, msg="lovely SPAM"),
            log_record(level=level, msg="Trouble at the mill!"),
            log_record(level=level, msg="Wonderful SPAM"),
        ]
        expect(log.find_log_records(level=level, partial_text="SPAM")).to(
            equal([log.stored_records[0], log.stored_records[2]])
        )

    def test_returns_empty_when_level_does_not_match(self):
        log = FakeLogging()
        log.stored_records = [log_record(level=logging.INFO, msg="There's some lovely filth down here!")]
        expect(log.find_log_records(level=logging.WARNING, partial_text="lovely")).to(be_empty)

    def test_ignores_level_when_unspecified(self):
        log = FakeLogging()
        log.stored_records = [
            log_record(level=logging.INFO, msg="This is not a match"),
            log_record(level=logging.INFO, msg="There's some lovely filth down here!"),
            log_record(level=logging.ERROR, msg="There's some lovely filth down here!"),
        ]
        expect(log.find_log_records(partial_text="lovely")).to(equal(log.stored_records[1:]))

    def test_ignores_partial_text_when_unspecified(self):
        log = FakeLogging()
        log.stored_records = [
            log_record(level=logging.INFO, msg="This is not a match"),
            log_record(level=logging.INFO, msg="There's some lovely filth down here!"),
            log_record(level=logging.ERROR, msg="There's some lovely filth down here!"),
        ]
        expect(log.find_log_records(level=logging.INFO)).to(equal(log.stored_records[0:2]))


if "__main__" == __name__:
    main()
