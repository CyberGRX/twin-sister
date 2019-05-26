from unittest import TestCase, main

from expects import expect, equal

from twin_sister import TimeController, \
    close_all_dependency_contexts, \
    dependency, dependency_context, open_dependency_context


class TestContextNesting(TestCase):

    def setUp(self):
        close_all_dependency_contexts()

    def test_inherited_with_context_manager(self):
        real_spam = 'real spam'
        fake_spam = 'injected spam'
        with dependency_context() as outer:
            outer.inject(real_spam, fake_spam)
            with dependency_context(parent=outer):
                expect(dependency(real_spam)).to(equal(fake_spam))

    def test_direct_with_context_manager(self):
        real_spam = 'real spam'
        fake_spam = 'injected spam'
        with dependency_context() as outer:
            with dependency_context(parent=outer) as inner:
                inner.inject(real_spam, fake_spam)
                expect(dependency(real_spam)).to(equal(fake_spam))

    def test_parent_unaffected_by_child_injection(self):
        real_spam = 'real spam'
        fake_spam = 'injected spam'
        with dependency_context() as outer:
            with dependency_context(parent=outer) as inner:
                inner.inject(real_spam, fake_spam)
            expect(dependency(real_spam)).to(equal(real_spam))

    def test_reflects_changes_to_parent(self):
        real_spam = 'real spam'
        fake_1 = 'first injection'
        fake_2 = 'second injection'
        try:
            parent = open_dependency_context()
            parent.inject(real_spam, fake_1)
            child = open_dependency_context(parent=parent)
            parent.inject(real_spam, fake_2)
            expect(dependency(real_spam)).to(equal(fake_2))
        finally:
            child.close()
            parent.close()

    def test_time_controller(self):
        real_spam = 'real SPAM'
        fake_spam = 'phoney balogna'
        parent = open_dependency_context()
        try:
            parent.inject(real_spam, fake_spam)
            tc = TimeController(
                target=lambda: dependency(real_spam),
                parent_context=parent)
            tc.start()
            tc.join()
        finally:
            parent.close()
        if tc.exception_caught:
            raise tc.exception_caught
        expect(tc.value_returned).to(equal(fake_spam))

    def test_recursion(self):
        spam = 'SPAM'
        fake_spam = 'Advanced SPAM Substitute'
        one = open_dependency_context()
        one.inject(spam, fake_spam)
        two = open_dependency_context(parent=one)
        three = open_dependency_context(parent=two)
        try:
            expect(dependency(spam)).to(equal(fake_spam))
        finally:
            three.close()
            two.close()
            one.close()

    def test_precedence(self):
        spam = 'SPAM'
        inner_fake = 'inner fake'
        outer_fake = 'outer fake'
        with dependency_context() as outer:
            outer.inject(spam, outer_fake)
            with dependency_context(parent=outer) as inner:
                inner.inject(spam, inner_fake)
                expect(dependency(spam)).to(equal(inner_fake))


if '__main__' == __name__:
    main()
