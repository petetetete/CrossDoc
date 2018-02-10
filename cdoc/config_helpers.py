# Python Standard Library imports
import os
import json

# Our module imports
from .logging import Logger

# Constants
CONFIG_NAME = "cdoc-config.json"
DEFAULT_SET = "No Set"
ANCHOR_EXTENSION = ".json"
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

  # Get the path to the configuration file
  path = find_config_path(os.getcwd())

  if path is None:
    Logger.fatal("not in a CrossDoc project directory")

  with open(path, "r") as file:
    data = json.load(file)

  return data


def store_is_valid(store):
  """Determine whether a given store is valid"""

  return os.path.isdir(store)


def find_comment(anchor, store=None):
  """Find the comment in the specified store or any store

  Raises:
    ValueError: No valid comment stores found"""

  config = get_config()

  # If we weren't given a specific store to save to
  if store is None:
    curr_store = next((s for s in config["stores"] if store_is_valid(s)), None)

    if curr_store is None:
      raise ValueError("No valid comment stores found")

  # We were given a store to check
  else:
    # TODO: Look into better store reference
    store = int(store)
    if ((store >= 0 and store < len(config["stores"])) and
            store_is_valid(config["stores"][store])):
      curr_store = config["stores"][store]
    else:
      raise ValueError("Store specified is invalid")

  # Remove anchor hook if it exists
  if anchor.startswith(ANCHOR_HOOK):
    anchor = anchor[len(ANCHOR_HOOK):]

  # Find the matching anchor
  all_files = os.listdir(os.fsencode(curr_store))
  file_name = next((os.fsdecode(f) for f in all_files
                    if os.fsdecode(f) == anchor + ANCHOR_EXTENSION), None)

  # If we found a matching anchor
  if file_name is not None:
    file_path = os.path.join(curr_store, file_name)

    # Get json from anchor
    anchor_json = []
    if os.path.isfile(file_path) and os.stat(file_path).st_size != 0:
      with open(file_path) as file:
        anchor_json = json.load(file)

    return file_path, anchor_json

  # No anchor found
  else:
    raise ValueError("Anchor not found")


def add_anchor_prefix(anchor):
  """Prefix anchor with hook if missing it"""

  if anchor.startswith(ANCHOR_HOOK):
    return anchor
  else:
    return ANCHOR_HOOK + anchor


def find_config_path(base):
  """Recursively find path to the config file if it exists"""

  # Ensure that the given path is a directory
  curr_path = base if os.path.isdir(base) else os.path.dirname(base)

  # Iterate up from the given directory looking for the file
  while True:

    # If we found the config
    curr_check = os.path.join(curr_path, "cdoc-config.json")
    if os.path.isfile(curr_check):
      return curr_check

    # Break when we've hit the root
    if os.path.dirname(curr_path) == curr_path:
      break

    # Pop off a directory
    curr_path = os.path.dirname(curr_path)

  return None
