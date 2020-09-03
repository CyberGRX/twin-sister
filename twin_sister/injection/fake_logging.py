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

        logger = self.fake_logger("")
        for name in ("critical", "error", "exception", "warning", "info", "debug"):
            setattr(self, name, getattr(logger, name))

    def StreamHandler(self, *args, **kwargs):
        return FakeHandler(fake_module=self)

    def fake_logger(self, name):
        logger = logging.Logger(name)
        logger.handlers = [self.StreamHandler()]
        return logger

    def find_log_records(self, *, level=None, partial_text=None):
        return [
            rec
            for rec in self.stored_records
            if ((level is None or rec.levelno == level) and (partial_text is None or partial_text in rec.msg))
        ]

    Logger = fake_logger
    getLogger = fake_logger

    def reset(self):
        self.stored_records = []
