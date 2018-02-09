# Python Standard Library imports
import random
import time
import hashlib
import os

# Our module imports
from .config_helpers import *
from .logging import Logger

# The parsing uses parameter annotations to match command line arguments
# to the appropriate parameters (including aliases).

# Also, the parsing interprets the lack of a default value as a required
# parameter, while setting a default value to a list will return a list of
# command line arguments, and setting the default to any other value will
# simply take the first value the user gives


def project_init(name: "-name -n" = "Default Project Name",
                 stores: "-stores -s" = []) -> "init i":

  config = {
    "project_name": name,
    "stores": stores
  }

  try:
    create_config(config)
  except FileExistsError:
    Logger.fatal("configuration file already exists")

  return CONFIG_NAME + " initialized in this directory"


def generate_anchor() -> "generate-anchor ga g":

  hash_length = 16
  string_to_hash = str(time.time()) + "|" + str(random.uniform(0, 1))
  final_hash = hashlib.md5(string_to_hash.encode("utf-8")).hexdigest()

  return ANCHOR_HOOK + final_hash[:hash_length]


def create_comment(text: "-text -t",
                   store: "-store -st" = None,  # Referenced by index
                   anchor: "-anchor -a" = None,
                   set: "-set" = None) -> "create-comment cc c":

  config = get_config()
  if len(config["stores"]) == 0:
    Logger.fatal("no comment stores to create to")

  # If we weren't given a specific store to save to
  if store is None:

    # Find first store that exists
    i = 0
    while (i < len(config["stores"]) and
           not store_is_valid(config["stores"][i])):
      i += 1

    # We couldn't find a valid store
    if i >= len(config["stores"]):
      Logger.fatal("no valid comment stores found")

    curr_store = config["stores"][i]

  # We were given a store to check
  else:
    # TODO: Look into better store reference
    if (int(store) < len(config["stores"]) and
            store_is_valid(config["stores"][int(store)])):
      curr_store = config["stores"][int(store)]
    else:
      curr_store = ""
      Logger.fatal("store specified is invalid")

  # Determine the set and anchors to use
  set_to_use = DEFAULT_SET if set is None else set
  anchor_to_use = generate_anchor() if anchor is None else anchor

  # Remove anchor hook from path if present
  if anchor_to_use.startswith(ANCHOR_HOOK):
    file_name = anchor_to_use[len(ANCHOR_HOOK):]
  else:
    file_name = anchor_to_use
    anchor_to_use = ANCHOR_HOOK + anchor_to_use

  file_path = curr_store + "/" + file_name + ANCHOR_EXTENSION

  # Create list to store sets or get it if it already exists
  anchor_json = []
  if os.path.isfile(file_path) and os.stat(file_path).st_size != 0:
    with open(file_path) as file:
      anchor_json = json.load(file)

  # Replace existing set or add new set
  found_set = next((s for s in anchor_json if s["set"] == set_to_use), None)
  if found_set:
    found_set["comment"] = text
  else:
    anchor_json.append({"set": set_to_use, "comment": text})

  with open(file_path, "w") as file:
    json.dump(anchor_json, file, indent=4)

  return anchor_to_use


def fetch_comment(anchor: "-anchor -a",
                  store: "-store -s" = None) -> "fetch-comment fc f":

  try:
    filePath, start, end = find_comment(anchor, store)
  except ValueError:
    Logger.fatal("comment anchor not found")

  with open(filePath) as file:
    return "".join(file.readlines()[start + 1:end]).rstrip("\n")


def delete_comment(anchor: "-anchor -a",
                   store: "-store -s" = None) -> "delete-comment dc d":

  try:
    filePath, start, end = find_comment(anchor, store)
  except ValueError:
    Logger.fatal("comment anchor not found")

  with open(filePath, "r+") as file:
    lines = file.readlines()
    file.seek(0)
    file.writelines(lines[0:start] + lines[end:])
    file.truncate()

  return "comment at " + anchor + " deleted"


def update_comment(anchor: "-anchor -a",
                   text: "-text -t" = "",
                   store: "-store -s" = None) -> "update-comment uc u":

  try:
    filePath, start, end = find_comment(anchor, store)
  except ValueError:
    Logger.fatal("comment anchor not found")

  with open(filePath, "r+") as file:
    lines = file.readlines()
    file.seek(0)
    file.writelines(lines[0:start + 1] + [text + "\n", "\n"] + lines[end:])
    file.truncate()

  return "comment at " + anchor + " updated"
