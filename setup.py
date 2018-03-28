import os
from setuptools import Command, setup, find_packages
from unittest import TestLoader

MAJOR_VERSION = 1
MINOR_VERSION = 4
PATCH_VERSION = 0

# Environment variable into which CI places the build ID
# https://docs.gitlab.com/ce/ci/variables/
CI_BUILD_ID = 'BUILD_NUMBER'


class TestRunner(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # If we perform this input at the top of the file, we get an
        # import error because we need to load this file to discover
        # dependenices.
        from xmlrunner import XMLTestRunner
        tests = TestLoader().discover('tests', pattern='test_*.py')
        runner = XMLTestRunner(output='reports')
        runner.run(tests)


def set_build_number_from_ci_environment():
    return int(os.environ[CI_BUILD_ID])


def version_number():
    if CI_BUILD_ID in os.environ:
        build = set_build_number_from_ci_environment()
    else:
        build = 0
    return '%d.%d.%d.%d' % (MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION, build)


setup(name='younger_twin_sister',
      version=version_number(),
      description='Simplifies dependency injection',
      author='Mike Duskis',
      author_email='mike.duskis@cybergrx.com',
      license='',
      packages=find_packages(),
      include_package_data=True,
      exclude_package_data={'': ['tests']},
      install_requires=[
        'expects>=0.8.0',
        'twine>=1.9.1',
        'unittest-xml-reporting-2.1.1',
        'wheel>=0.3.0'
        ],
      cmdclass={'test': TestRunner},
      )
