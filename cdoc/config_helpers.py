# Python Standard Library imports
import os
import json

# Our module imports
from .logging import *

# Constants
CONFIG_NAME = "cdoc-config.json"


def createConfig(data):
  """Create configuration file

  Raises:
    FileExistsError: Configuration file already exists"""

  if os.path.isfile(CONFIG_NAME):
    raise FileExistsError("Config file already exists")

  output = open(CONFIG_NAME, "w")
  json.dump(data, output, indent=4, separators=(',', ': '), sort_keys=True)

  return


def getConfig():
  try:
    with open("cdoc-config.json", "r") as file:
      data = json.load(file)

  except FileNotFoundError:
    logFatal("not in a CrossDoc project directory")

  return data
