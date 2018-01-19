Development Notes
=================

This document contains important development notes that can be used as a
reference sheet for frequently used commands and processes. If you are
looking for initial setup instructions, the `contributing write-up`_
should be your starting point.

Running Tests
-------------

The following command runs **all** of the test modules:
``python setup.py test``

To run specific test modules, use the following commands:

-  Unit Tests: ``python setup.py test --test-suite=tests.unit``
-  Integration Tests:
   ``python setup.py test --test-suite=tests.integration``

Package Updating
----------------

Steps to creating and uploading a Pip update:

-  Tag release: ``git tag <x.y.z> -m <message>``
-  Push tag: ``git push --tags``
-  Setup distributions: ``python setup.py sdist``
-  Upload to pypi.org: ``twine upload dist/*``

   -  Upload to test.pypi.org:
      ``twine upload --repository testpypi dist/*``

These steps assume that a .pypirc has already been setup that matches
the following pattern:

::

    [distutils]
    index-servers =
      pypi
      testpypi

    [pypi]
    username=<username>
    password=<password>

    [testpypi]
    repository=https://test.pypi.org/legacy/
    username=<username>
    password=<password>

.. _contributing write-up: CONTRIBUTING.rst
