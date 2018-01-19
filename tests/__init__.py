import unittest
import tests.unit_tests
import tests.integration_tests


def all():
  # Get all of the test suites
  suites = []
  suites.append(loader.loadTestsFromModule(tests.unit_tests))
  suites.append(loader.loadTestsFromModule(tests.integration_tests))

  return unittest.TestSuite(suites)


def unit():
  return loader.loadTestsFromModule(tests.unit_tests)


def integration():
  return loader.loadTestsFromModule(tests.integration_tests)


loader = unittest.TestLoader()
