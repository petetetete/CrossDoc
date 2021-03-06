import os
from setuptools import setup


def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='cross-doc',
      version='0.2.0',
      description='A comment management system for the modern world',
      long_description=read('README.rst'),
      author='Octo-Docs',
      author_email='ph289@nau.edu',
      license='MIT',
      url='https://github.com/petetetete/CrossDoc',
      download_url='https://github.com/petetetete/CrossDoc/archive/0.2.0.tar.gz',
      keywords='CrossDoc documentation comments storage',
      packages=['cdoc'],
      test_suite='tests.all',
      entry_points={
        'console_scripts': [
          'cross-doc = cdoc.__main__:main',
          'cdoc = cdoc.__main__:main'
        ]
      })
