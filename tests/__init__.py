import os
import unittest
import tests.unit_tests
import tests.integration_tests


def all():

  # Get all of the test suites
  suites = []
  suites.append(unit())
  suites.append(integration())

  return unittest.TestSuite(suites)


def unit():

  # Navigate up from the current working directory
  os.chdir(os.path.dirname(os.getcwd()))
  return loader.loadTestsFromModule(tests.unit_tests)


def integration():
  return loader.loadTestsFromModule(tests.integration_tests)


loader = unittest.TestLoader()
