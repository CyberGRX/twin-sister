from threading import Thread
from unittest import TestCase, main

from expects import expect, be, raise_error

from twin_sister import dependency, dependency_context


class TwoStageThread(Thread):
    """
    Thread that runs in two stages:
    1. Launch the thread but do nothing else
    2. Run the target function

    This enables us to grab the ID of the thread before it runs the target.
    """

    def __init__(self, target, **kwargs):
        super().__init__(**kwargs)
        self._target = target
        self._free = False

    def really_start(self):
        self._free = True

    def run(self):
        while not self._free:
            pass
        self._target()


class TestAttachContextToThread(TestCase):

    def test_sees_injected_dependency(self):
        real_thing = 'real thing'
        injected_thing = 'injected thing'
        thing_seen_by_thread = None

        def canary():
            nonlocal thing_seen_by_thread
            thing_seen_by_thread = dependency(real_thing)
        t = TwoStageThread(target=canary, daemon=True)
        t.start()

        with dependency_context() as context:
            context.inject(real_thing, injected_thing)
            context.attach_to_thread(t)
            t.really_start()
            t.join()
        expect(thing_seen_by_thread).to(be(injected_thing))

    def test_complains_if_thread_not_started(self):
        with dependency_context() as context:
            def attempt():
                context.attach_to_thread(Thread(target=print))
            expect(attempt).to(raise_error(RuntimeError))

    def test_stops_seeing_injection_when_context_ends(self):
        real_thing = 'real thing'
        injected_thing = 'injected thing'
        thing_seen_by_thread = None

        def canary():
            nonlocal thing_seen_by_thread
            thing_seen_by_thread = dependency(real_thing)
        t = TwoStageThread(target=canary, daemon=True)
        t.start()

        with dependency_context() as context:
            context.inject(real_thing, injected_thing)
            context.attach_to_thread(t)
        t.really_start()
        t.join()
        expect(thing_seen_by_thread).to(be(real_thing))


if '__main__' == __name__:
    main()
