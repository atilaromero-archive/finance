'''
finance: finance indexes in python

Note that "python setup.py test" invokes pytest on the package. With appropriately
configured setup.cfg, this will check both xxx_test modules and docstrings.

Copyright 2014, Atila Romero.
Licensed under GNU AFFERO GENERAL PUBLIC LICENSE.
'''
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit(pytest.main(self.test_args))


version = "0.1"

setup(name="finance",
      version=version,
      description="finance indexes in python",
      long_description=open("README.rst").read(),
      classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Programming Language :: Python'
      ],
      keywords="finance python blackscholes options", # Separate with spaces
      author="Atila Romero",
      author_email="atilaromero@gmail.com",
      url="http://github.com/atilaromero/finance",
      license="GNU AFFERO GENERAL PUBLIC LICENSE",
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      tests_require=['pytest'],
      cmdclass={'test': PyTest},
      
      # TODO: List of packages that this one depends upon:   
      install_requires=[],
      # TODO: List executable scripts, provided by the package (this is just an example)
      entry_points={
        'console_scripts': 
            ['finance=finance:main']
      }
)
