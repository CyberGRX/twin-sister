import os
from unittest import TestCase, main

from expects import expect, be, be_a, equal
from pyfakefs import fake_filesystem as fakefs

from twin_sister import dependency, dependency_context
from twin_sister.injection.dependency_context import DependencyContext


class TestFakeFilesystem(TestCase):

    def test_creates_filesystem_when_requested(self):
        with dependency_context(supply_fs=True) as context:
            expect(context.fs).to(be_a(fakefs.FakeFilesystem))

    def test_provides_reference_to_fake_os(self):
        with dependency_context(supply_fs=True) as context:
            expect(context.os).to(be_a(fakefs.FakeOsModule))

    def test_injects_fake_os(self):
        with dependency_context(supply_fs=True) as context:
            expect(context.os).to(be(dependency(os)))

    def test_provides_reference_to_fake_os_path(self):
        with dependency_context(supply_fs=True) as context:
            expect(context.os.path).to(be_a(fakefs.FakePathModule))

    def test_injects_fake_os_path(self):
        with dependency_context(supply_fs=True) as context:
            expect(dependency(os.path)).to(be(context.os.path))

    def test_supplies_real_os_path_when_fake_not_requested(self):
        with dependency_context():
            expect(dependency(os.path)).to(be(os.path))

    def test_supplies_real_os_when_fake_not_requested(self):
        with dependency_context():
            # We don't care about the identity of os.
            # We do care about the identity of its attributes.
            expect(dependency(os).getpid).to(be(os.getpid))

    def test_references_refer_to_same_fake(self):
        fname = 'baloney.txt'
        with dependency_context(supply_fs=True) as context:
            f = context.os.open(fname, flags=os.O_CREAT)
            context.os.close(f)
            assert context.os.path.exists(fname), 'File not found'

    def test_does_not_create_filesystem_when_not_requested(self):
        with dependency_context() as context:
            expect(context.fs).to(equal(None))

    def test_injects_open(self):
        fname = 'reginald'
        planted = b'some rubbish from test_fake_filesystem'
        with dependency_context(supply_fs=True) as context:
            # Write
            f = context.os.open(
                fname,
                flags=os.O_CREAT | os.O_WRONLY)
            context.os.write(f, planted)
            context.os.close(f)
            # Read
            try:
                with dependency(open)(fname, 'rb') as f:
                    expect(f.read()).to(equal(planted))
            except FileNotFoundError:
                assert False, '"open" not find fake file'

    def test_provides_create_file_convenience(self):
        planted = b'yummy fig leaves'
        with dependency_context(supply_fs=True) as context:
            filename = context.os.path.join('a', 'b', 'c.this')
            context.create_file(filename, content=planted)
            f = context.os.open(filename, flags=os.O_RDONLY)
            expect(context.os.read(f, len(planted))).to(
                equal(planted))

    def test_create_file_can_create_two_files_in_same_path(self):
        """
        Verifies that os.makedirs gets called with exist_ok=True
        """
        with dependency_context(supply_fs=True) as context:
            join = context.os.path.join
            path = join('somewhere', 'nice')
            context.create_file(join(path, 'a'), content=b'a')
            caught = None
            try:
                context.create_file(join(path, 'b'), content=b'b')
            except FileExistsError as e:
                caught = e
            expect(caught).to(equal(None))

    def test_create_file_accepts_strings(self):
        planted = 'some text'
        filename = 'yad.dah'
        with dependency_context(supply_fs=True) as context:
            context.create_file(filename, text=planted)
            with dependency(open)(filename, 'r') as f:
                expect(f.read()).to(equal(planted))

    def test_creates_empty_file_if_neither_text_nor_content(self):
        filename = 'an-empty-file'
        with dependency_context(supply_fs=True) as context:
            context.create_file(filename)
            with dependency(open)(filename, 'rb') as f:
                expect(f.read()).to(equal(b''))

    def test_complains_if_both_text_and_content(self):
        with dependency_context(supply_fs=True) as context:
            caught = None
            try:
                context.create_file('s', content=b'a', text='b')
            except TypeError as e:
                caught = e
            expect(caught).not_to(equal(None))

    def test_complains_about_attempt_to_mix_with_parent_context(self):
        try:
            DependencyContext(parent=DependencyContext(), supply_fs=True)
            assert False, 'No exception was raised'
        except ValueError:
            pass


if '__main__' == __name__:
    main()
