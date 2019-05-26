from unittest import TestCase, main

from expects import expect, equal

from twin_sister.expects_matchers import complain, raise_ex


class TestAliases(TestCase):

    def test_complain(self):
        expect(complain).to(equal(raise_ex))


if '__main__' == __name__:
    main()
