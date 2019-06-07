import os
from setuptools import setup, find_packages
from setuptools.command.test import test
from unittest import TestLoader

MAJOR_VERSION = 4
MINOR_VERSION = 3
PATCH_VERSION = 0

# Environment variable into which CI places the build ID
# https://docs.gitlab.com/ce/ci/variables/
CI_BUILD_ID = 'BUILD_NUMBER'


class TestRunner(test):

    def run_tests(self):
        # If we perform this input at the top of the file, we get an
        # import error because we need to load this file to discover
        # dependenices.
        from xmlrunner import XMLTestRunner
        tests = TestLoader().discover('tests', pattern='test_*.py')
        runner = XMLTestRunner(output='reports')
        result = runner.run(tests)
        exit(0 if result.wasSuccessful() else 1)


def set_build_number_from_ci_environment():
    return int(os.environ[CI_BUILD_ID])


def version_number():
    if CI_BUILD_ID in os.environ:
        build = set_build_number_from_ci_environment()
    else:
        build = 0
    return '%d.%d.%d.%d' % (MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION, build)


with open('README.md', 'r') as f:
    long_description = f.read()


setup(name='twin_sister',
      version=version_number(),
      description='Unit test toolkit',
      url='https://github.com/CyberGRX/twin-sister',
      author='Mike Duskis',
      author_email='mike.duskis@cybergrx.com',
      license='',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=find_packages(),
      include_package_data=True,
      exclude_package_data={'': ['tests']},
      install_requires=[
        'expects>=0.8.0',
        'pyfakefs>=3.4.3',
        'twine>=1.9.1',
        'unittest-xml-reporting>=2.1.1',
        'wheel>=0.30.0'
        ],
      cmdclass={'test': TestRunner}
      )
