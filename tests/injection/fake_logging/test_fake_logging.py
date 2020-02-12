import logging
from unittest import TestCase, main
import sys

from expects import expect, be, be_a, be_empty, contain, equal, have_length

from twin_sister import dependency, dependency_context
from twin_sister.injection.dependency_context import DependencyContext
import twin_sister.injection.fake_logging as fake_logging
from twin_sister.injection.passthrough import Passthrough

FakeLogging = fake_logging.FakeLogging


class TestFakeLogging(TestCase):

    def test_does_not_supply_fake_unless_specified(self):
        with dependency_context():
            expect(dependency(logging)).to(be(logging))

    def test_logging_is_fake(self):
        with dependency_context(supply_logging=True):
            expect(dependency(logging)).to(be_a(FakeLogging))

    def test_fake_logging_is_passthrough_to_real_logging(self):
        with dependency_context(supply_logging=True):
            injected = dependency(logging)
            expect(injected).to(be_a(Passthrough))
            expect(injected._target).to(be(logging))

    def test_injects_fake_logger_as_getlogger(self):
        with dependency_context(supply_logging=True) as context:
            expected = context.logging.fake_logger
            injected = dependency(logging).getLogger
            expect(injected).to(equal(expected))

    def test_injects_fake_logger_as_logger(self):
        with dependency_context(supply_logging=True) as context:
            expect(dependency(logging).Logger).to(
                equal(context.logging.fake_logger))

    def test_fake_logger_returns_a_logger(self):
        expect(FakeLogging().fake_logger('')).to(be_a(logging.Logger))

    def test_injects_fake_handler_as_streamhandler(self):
        with dependency_context(supply_logging=True):
            expect(dependency(logging).StreamHandler(stream=sys.stderr)).to(
                be_a(fake_logging.FakeHandler))

    def test_fake_logger_has_provided_module_name(self):
        module_name = 'my_fancy_module'
        expect(FakeLogging().fake_logger(module_name).name).to(
            equal(module_name))

    def test_logger_has_exactly_one_handler(self):
        handlers = FakeLogging().fake_logger('').handlers
        expect(handlers).to(have_length(1))
        expect(handlers[0]).to(be_a(logging.Handler))

    def test_handler_saves_log_record(self):
        fake_module = FakeLogging()
        fake_module.fake_logger('something').info('something')
        records = fake_module.stored_records
        expect(records).to(have_length(1))
        expect(records[0]).to(be_a(logging.LogRecord))

    def test_handler_saves_records_in_sequence(self):
        fake_module = FakeLogging()
        logger = fake_module.fake_logger('something')
        messages = ['Albatross!', 'Seagullsickles!', 'Pelican Bon Bons!']
        for msg in messages:
            logger.info(msg)
        recorded = [rec.msg for rec in fake_module.stored_records]
        expect(recorded).to(equal(messages))

    def test_handler_saves_debug_entry(self):
        # If it saves debug, we can infer that the log level is DEBUG
        # which means it will save other entries as well
        fake_module = FakeLogging()
        msg = 'We represent the Lollipop Guild'
        fake_module.getLogger('something').debug(msg)
        expect([r.msg for r in fake_module.stored_records]).to(
            contain(msg))

    def test_inherits_fake_from_parent_context(self):
        parent = DependencyContext(supply_logging=True)
        child = DependencyContext(parent=parent)
        expect(child.logging).to(be(parent.logging))

    def test_refuses_to_supply_logging_if_parent_specified(self):
        try:
            DependencyContext(parent=DependencyContext(), supply_logging=True)
            assert False, 'Caught nothing'
        except ValueError:
            pass  # Caught what we expected

    def test_reset_clears_stored_records(self):
        fake_module = FakeLogging()
        fake_module.fake_logger('something').error('oops')
        expect(fake_module.stored_records).not_to(be_empty)
        fake_module.reset()
        expect(fake_module.stored_records).to(be_empty)

    def check_convenience_method(self, name):
        fake = FakeLogging()
        getattr(fake, name)('spam')
        expect(fake.stored_records).to(have_length(1))
        expect(fake.stored_records[0].levelname).to(
            equal(name.upper()))

    def test_convenience_critical(self):
        self.check_convenience_method('critical')

    def test_convenience_error(self):
        self.check_convenience_method('error')

    def test_convenience_warning(self):
        self.check_convenience_method('warning')

    def test_convenience_info(self):
        self.check_convenience_method('info')

    def test_convenience_debug(self):
        self.check_convenience_method('debug')

    def test_convenience_exception(self):
        fake = FakeLogging()
        fake.exception('spam')
        expect(fake.stored_records).to(have_length(1))
        expect(fake.stored_records[0].levelname).to(equal('ERROR'))


if '__main__' == __name__:
    main()
