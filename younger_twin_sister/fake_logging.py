import logging

from .passthrough import Passthrough


class FakeHandler(logging.Handler):

    def __init__(self, *, fake_module):
        super().__init__()
        self._fake_module = fake_module

    def emit(self, record):
        self._fake_module.stored_records.append(record)


class FakeLogging(Passthrough):

    def __init__(self):
        super().__init__(target=logging)
        self.stored_records = []

    def fake_logger(self, name):
        logger = logging.Logger(name)
        logger.handlers = [FakeHandler(fake_module=self)]
        return logger

    Logger = fake_logger
    getLogger = fake_logger

    def reset(self):
        self.stored_records = []
