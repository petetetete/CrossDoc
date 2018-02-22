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
                   set: "-set" = DEFAULT_SET) -> "create-comment cc c":

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

  # Determine the anchor to use
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
  found_set = next((s for s in anchor_json if s["set"] == set), None)
  if found_set:
    found_set["comment"] = text
  else:
    anchor_json.append({"set": set, "comment": text})

  with open(file_path, "w") as file:
    json.dump(anchor_json, file, indent=4, sort_keys=True)

  return anchor_to_use + " [" + set + "]" + "\n" + text


def fetch_comment(anchor: "-anchor -a",
                  store: "-store -s" = None,
                  set: "-set" = DEFAULT_SET) -> "fetch-comment fc f":

  try:
    file_path, anchor_json = find_comment(anchor, store)
  except ValueError:
    Logger.fatal("comment anchor not found")

  found_set = next((s for s in anchor_json if s["set"] == set), None)
  if found_set:
    return found_set["comment"]
  else:
    Logger.fatal("comment set not found")


def delete_comment(anchor: "-anchor -a",
                   store: "-store -s" = None,
                   set: "-set" = None) -> "delete-comment dc d":

  try:
    file_path, anchor_json = find_comment(anchor, store)
  except ValueError:
    Logger.fatal("comment anchor not found")

  # If no set specified, delete the whole comment
  if set is None:
    os.remove(file_path)
    return "anchor \"" + add_anchor_prefix(anchor) + "\" deleted"

  # If we only want to delete a specific set
  else:

    # Find index of set to delete
    set_i = next((i for i, s in enumerate(anchor_json)
                  if s["set"] == set), None)

    # Fail if not found
    if set_i is None:
      Logger.fatal("comment set not found")

    # Delete set and update json
    else:
      set_name = anchor_json[set_i]["set"]
      del anchor_json[set_i]

      with open(file_path, "w") as file:
        json.dump(anchor_json, file, indent=4, sort_keys=True)

      return ("set \"" + set_name + "\" at \"" +
              add_anchor_prefix(anchor) + "\" deleted")


def update_comment(anchor: "-anchor -a",
                   text: "-text -t",
                   store: "-store -s" = None,
                   set: "-set" = DEFAULT_SET) -> "update-comment uc u":

  try:
    file_path, anchor_json = find_comment(anchor, store)
  except ValueError:
    Logger.fatal("comment anchor not found")

  set_i = next((i for i, s in enumerate(anchor_json)
                if s["set"] == set), None)

  # Fail if not found
  if set_i is None:
    Logger.fatal("comment set not found")

  # Update set and update json
  else:
    anchor_json[set_i]["comment"] = text

    with open(file_path, "w") as file:
      json.dump(anchor_json, file, indent=4, sort_keys=True)

  return ("set \"" + anchor_json[set_i]["set"] + "\" at \"" +
          add_anchor_prefix(anchor) + "\" updated")
