# Python Standard Library imports
import os
import json

# Our module imports
from .logging import Logger

# Constants
CONFIG_NAME = "cdoc-config.json"
DEFAULT_SET = "No Set"
SET_EXTENSION = ".txt"
ANCHOR_HOOK = "<&> "


def create_config(data):
  """Create configuration file

  Raises:
    FileExistsError: Configuration file already exists"""

  if os.path.isfile(CONFIG_NAME):
    raise FileExistsError("Config file already exists")

  output = open(CONFIG_NAME, "w")
  json.dump(data, output, indent=4, separators=(',', ': '), sort_keys=True)

  return


def get_config():
  """Trys to open the config file"""

  try:
    with open("cdoc-config.json", "r") as file:
      data = json.load(file)

  except FileNotFoundError:
    Logger.fatal("not in a CrossDoc project directory")

  return data


def store_is_valid(store):
  """Determine whether a given store is valid"""

  return os.path.isdir(store)


def find_comment(anchor, store=None):
  """Finds comment through stores or in a specific store

  Raises:
    ValueError: No matching comment found"""

  config = get_config()

  for i, cStore in enumerate(config["stores"]):
    if not store_is_valid(cStore) or store is not None and i != int(store):
      continue

    # Loop through all sets in the store
    for file in os.listdir(os.fsencode(cStore)):
      set = os.fsdecode(file)

      # Skip files that are not sets
      if not set.endswith(SET_EXTENSION):
        continue

      filePath = os.path.join(cStore, set)
      with open(filePath) as file:

        lines = file.readlines()
        start = next((i for i, l in enumerate(lines)
                      if l.strip("\n").replace(ANCHOR_HOOK, "") == anchor),
                     None)

        if start is not None:
          end = next((i for i, l in enumerate(lines[start + 1:])
                      if ANCHOR_HOOK in l),
                     None)

          if end is None:
            return filePath, start, len(lines)
          else:
            return filePath, start, start + end + 1

  raise ValueError("No matching comment found")
