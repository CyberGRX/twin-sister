from pyfakefs import fake_filesystem as api


def create_fs():
    return api.FakeFilesystem()


def create_open(fs):
    return api.FakeFileOpen(fs)


def create_os(fs):
    return api.FakeOsModule(fs)
