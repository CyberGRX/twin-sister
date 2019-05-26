import os
from unittest import TestCase, main

from expects import expect, be

from twin_sister import dependency, dependency_context


class TestUnhashableDependency(TestCase):

    def test_can_replace_unhashable(self):
        with dependency_context() as context:
            thing = object()
            context.inject(os.environ, thing)
            expect(dependency(os.environ)).to(be(thing))

    def test_survives_mutation(self):
        with dependency_context() as context:
            dep = ['spam', 'eggs', 'sausage']
            thing = object()
            context.inject(dep, thing)
            dep.append('spam')
            expect(dependency(dep)).to(be(thing))


if '__main__' == __name__:
    main()
