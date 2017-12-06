# Python Standard Library imports
from pprint import pprint

# Our module imports
from .config_helpers import *
from .logging import *


def projectInit():
  default = {
    "project_name": "Default Project Name",
    "sources": []
  }

  try:
    createConfig(default)

  except FileExistsError:
    logFatal("configuration file already exists")

  return


def createComment():

  pprint(getConfig())

  return
