from unittest import TestCase, main

from expects import expect, be_a

from twin_sister.expects_matchers import complain
from twin_sister.fakes import EmptyFake, empty_context_manager


class TestEmptyContextManager(TestCase):

    def test_accepts_arbitrary_args_and_kwargs(self):

        def attempt():
            with empty_context_manager(7, spams=2):
                pass

        expect(attempt).not_to(complain(TypeError))

    def test_yields_an_empty_fake(self):
        with empty_context_manager() as actual:
            expect(actual).to(be_a(EmptyFake))


if '__main__' == __name__:
    main()
