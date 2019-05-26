from threading import Thread
from unittest import TestCase, main

from expects import expect, be_false, be_true

from twin_sister import close_all_dependency_contexts, dependency, \
    open_dependency_context
from twin_sister.injection.singleton_class import SingletonClass


class Canary:
    def __init__(self):
        self.touched = False

    def touch(self):
        self.touched = True


def touch_a_canary():
    dependency(Canary)().touch()


class TestInjection(TestCase):

    def tearDown(self):
        close_all_dependency_contexts()

    def test_simple_injection(self):
        my_canary = Canary()
        context = open_dependency_context()
        context.inject(Canary, SingletonClass(my_canary))
        touch_a_canary()
        context.close()
        expect(my_canary.touched).to(be_true)

    def test_uses_object_injected_at_top_of_stack(self):
        bottom_canary = Canary()
        top_canary = Canary()
        bottom_context = open_dependency_context()
        bottom_context.inject(Canary, SingletonClass(bottom_canary))
        top_context = open_dependency_context()
        top_context.inject(Canary, SingletonClass(top_canary))
        touch_a_canary()
        top_context.close()
        expect(top_canary.touched).to(be_true)
        bottom_context.close()

    def test_does_not_use_object_injected_lower_in_stack(self):
        bottom_canary = Canary()
        top_canary = Canary()
        bottom_context = open_dependency_context()
        bottom_context.inject(Canary, SingletonClass(bottom_canary))
        top_context = open_dependency_context()
        top_context.inject(Canary, SingletonClass(top_canary))
        touch_a_canary()
        top_context.close()
        bottom_context.close()
        expect(bottom_canary.touched).to(be_false)

    def test_pops_top_layer_off_the_stack(self):
        bottom_canary = Canary()
        top_canary = Canary()
        bottom_context = open_dependency_context()
        bottom_context.inject(Canary, SingletonClass(bottom_canary))
        top_context = open_dependency_context()
        top_context.inject(Canary, SingletonClass(top_canary))
        top_context.close()
        touch_a_canary()
        bottom_context.close()
        expect(bottom_canary.touched).to(be_true)

    def test_popped_layer_is_no_longer_used(self):
        bottom_canary = Canary()
        top_canary = Canary()
        bottom_context = open_dependency_context()
        bottom_context.inject(Canary, SingletonClass(bottom_canary))
        top_context = open_dependency_context()
        top_context.inject(Canary, SingletonClass(top_canary))
        top_context.close()
        touch_a_canary()
        bottom_context.close()
        expect(top_canary.touched).to(be_false)

    def test_injection_does_not_affect_another_thread(self):
        my_canary = Canary()
        context = open_dependency_context()
        context.inject(Canary, SingletonClass(my_canary))
        t = Thread(target=touch_a_canary)
        t.start()
        t.join()
        context.close()
        expect(my_canary.touched).to(be_false)


if '__main__' == __name__:
    main()
