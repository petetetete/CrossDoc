import sys
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

    # Clear test environment if it exists
    if os.path.isdir(cwd):
      shutil.rmtree(cwd)

    # Make and navigate to test environment
    os.makedirs(cwd)
    os.chdir(cwd)

    sys.stdout = None  # Disable any printing

  def tearDown(self):

    # Delete test environment
    cwd = os.getcwd()
    os.chdir(os.path.dirname(cwd))
    shutil.rmtree(cwd)

  # generate_anchor tests

  def test_generate_anchor(self):

    anchors = set()

    # Generate 100 anchors and ensure that they are all different
    for i in range(100):
      anchor = generate_anchor()
      self.assertNotIn(anchor, anchors)
      anchors.add(anchor)

  # init tests

  def test_init(self):

    project_init()

    config_file = os.path.join(os.getcwd(), "cdoc-config.json")
    self.assertTrue(os.path.isfile(config_file))

  def test_init_duplicate(self):

    project_init()

    with self.assertRaises(SystemExit):
      project_init()

  # create_store tests

  def test_create_store_not_init(self):

    with self.assertRaises(SystemExit):
      create_store()

  def test_create_store_no_params(self):

    project_init()
    create_store()

    self.assertTrue(os.path.isdir(os.path.join(os.getcwd(), "cdoc-store")))

  def test_create_store_name(self):

    store_name = "My New Store"

    project_init()
    create_store(store_name)

    self.assertTrue(os.path.isdir(os.path.join(os.getcwd(), store_name)))

  def test_create_store_path(self):

    store_path = os.path.join(os.getcwd(), "store_repo")
    os.makedirs(store_path)

    project_init()
    create_store(path=store_path)

    self.assertTrue(os.path.isdir(os.path.join(store_path, "cdoc-store")))

  def test_create_store_name_and_path(self):

    store_name = "Example naaaame"
    store_path = os.path.join(os.getcwd(), "store_repo")
    os.makedirs(store_path)

    project_init()
    create_store(store_name, store_path)

    self.assertTrue(os.path.isdir(os.path.join(store_path, store_name)))

  # create_comment tests

  def test_create_comment_no_params(self):

    with self.assertRaises(TypeError):
      create_comment()

  def test_create_comment_not_init(self):

    with self.assertRaises(SystemExit):
      create_comment("Example")

  def test_create_comment(self):

    project_init()
    create_store()
    create_comment("My new comment")

  # fetch_comment tests

  def test_fetch_comment_no_params(self):

    with self.assertRaises(TypeError):
      fetch_comment()

  def test_fetch_comment_not_init(self):

    with self.assertRaises(SystemExit):
      fetch_comment("555")

  def test_fetch_comment_no_comment(self):

    project_init()
    create_store()

    with self.assertRaises(SystemExit):
      fetch_comment("98796")

  def test_fetch_comment(self):

    project_init()
    create_store()

    create_comment("An example comment", anchor="dfa89")
    fetch_comment("dfa89")
