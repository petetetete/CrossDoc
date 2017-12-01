from setuptools import setup, find_packages

setup(name='cross-doc',
      version='0.0.1',
      description='CrossDoc comment management system',
      url='https://github.com/petetetete/CrossDoc',
      author='Octo-Docs',
      license='MIT',
      packages=find_packages(),
      entry_points={
        'console_scripts': [
          'cdoc = cdoc.__main__:main'
        ]
      })
