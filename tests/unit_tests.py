import os
import shutil
import unittest
from cdoc.registration import *
from cdoc.commands import generate_anchor, project_init, create_store


class TestUnitTests(unittest.TestCase):

  # Unit test environment management methods

  def setUp(self):

    # Create and navigate to test environment
    cwd = os.path.join(os.getcwd(), "cdoc_test_env")
    os.makedirs(cwd)
    os.chdir(cwd)

  def tearDown(self):

    # Delete test environment
    cwd = os.getcwd()
    os.chdir(os.path.dirname(cwd))
    shutil.rmtree(cwd)

  # Actual unit tests

  def test_generate_anchor(self):

    anchors = set()

    # Generate 100 anchors and ensure that they are all different
    for i in range(100):
      anchor = generate_anchor()
      self.assertNotIn(anchor, anchors)
      anchors.add(anchor)

  def test_init(self):

    project_init()

    config_file = os.path.join(os.getcwd(), "cdoc-config.json")
    self.assertTrue(os.path.isfile(config_file))

  def test_duplicate_init(self):

    project_init()

    with self.assertRaises(SystemExit):
      project_init()

  def test_create_store_not_init(self):

    with self.assertRaises(SystemExit):
      create_store()

  def test_create_store_no_params(self):

    project_init()
    create_store()
    self.assertTrue(os.path.isdir(os.path.join(os.getcwd(), "cdoc-store")))

  def test_create_store_with_name(self):

    project_init()
    create_store("My New Store")
    self.assertTrue(os.path.isdir(os.path.join(os.getcwd(), "My New Store")))
