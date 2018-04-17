import os
import unittest
from cdoc.registration import commands
from cdoc.commands import generate_anchor, project_init


class TestGenerateAnchor(unittest.TestCase):

  def test_unique(self):

    anchors = set()

    # Generate 100 anchors and ensure that they are all different
    for i in range(100):
      anchor = generate_anchor()
      self.assertNotIn(anchor, anchors)
      anchors.add(anchor)


class TestInit(unittest.TestCase):

  def test_config_created(self):

    project_init()

    config_file = os.path.join(os.getcwd(), "cdoc-config.json")
    self.assertTrue(os.path.isfile(config_file))

  def test_duplicate(self):

    with self.assertRaises(SystemExit):
      project_init()
