import os
import shutil
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

  # Find and create new testing environment
  test_env = os.path.join(os.path.dirname(os.getcwd()), "cdoc_test_env")

  if os.path.isdir(test_env):
    shutil.rmtree(test_env)

  os.makedirs(test_env)

  # Move to new testing environment
  os.chdir(test_env)

  return loader.loadTestsFromModule(tests.unit_tests)


def integration():
  return loader.loadTestsFromModule(tests.integration_tests)


loader = unittest.TestLoader()
