import os
from setuptools import setup


def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='cross-doc',
      version='0.0.1',
      description='A comment management system for the modern world',
      long_description=read('README.rst'),
      author='Octo-Docs',
      author_email='ph289@nau.edu',
      license='MIT',
      url='https://github.com/petetetete/CrossDoc',
      download_url='https://github.com/petetetete/CrossDoc/archive/0.0.1.tar.gz',
      keywords='CrossDoc documentation comments storage',
      packages=['cdoc'],
      entry_points={
        'console_scripts': [
          'cross-doc = cdoc.__main__:main',
          'cdoc = cdoc.__main__:main'
        ]
      })
