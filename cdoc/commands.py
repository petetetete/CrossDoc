# Python Standard Library imports
from pprint import pprint

# Our module imports
from .config_helpers import *
from .logging import *

# The parsing uses parameter annotations to match command line arguments
# to the appropriate parameters (including aliases).

# Also, the parsing interprets the lack of a default value as a required
# parameter, while setting a default value to a list will return a list of
# command line arguments, and setting the default to any other value will
# simply take the first value the user gives


def projectInit(name: "-name -n" = "Test"):
  print(name)

  default = {
    "project_name": "Default Project Name",
    "stores": []
  }

  try:
    createConfig(default)

  except FileExistsError:
    logFatal("configuration file already exists")

  return


def createComment(text: "-text -t", set: "-set -s" = ""):

  print(text)
  print(set)

  pprint(getConfig())

  return
