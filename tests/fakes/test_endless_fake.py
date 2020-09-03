from unittest import TestCase, main

from expects import expect, be

from twin_sister.fakes import EmptyFake, EndlessFake


class TestEndlessFake(TestCase):
    def test_is_an_alias_for_empty_fake(self):
        expect(EndlessFake).to(be(EmptyFake))


if "__main__" == __name__:
    main()
