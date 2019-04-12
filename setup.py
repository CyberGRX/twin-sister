import os
import subprocess
import sys

from setuptools import Command, setup, find_packages

MAJOR_VERSION = 2
MINOR_VERSION = 0
PATCH_VERSION = 4

# Environment variable into which CI places the build ID
# https://docs.gitlab.com/ce/ci/variables/
CI_BUILD_ID = 'CI_BUILD_ID'


class TestRunner(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        python = sys.executable
        p = subprocess.run(
            (python, '-m', 'unittest', 'discover', '-s', 'tests'))
        exit(p.returncode)


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
      description='Gentle dependency injection',
      url='https://github.com/CyberGRX/twin-sister',
      author='Mike Duskis',
      author_email='mike.duskis@cybergrx.com',
      license='',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=find_packages(),
      include_package_data=True,
      exclude_package_data={'': ['tests']},
      cmdclass={'test': TestRunner},
      install_requires=[
       'expects>=0.8.0',  # required by unit tests
       'twine>=1.9.1',  # required by setup
       'wheel>=0.30.0'  # required by setup
	]
      )
