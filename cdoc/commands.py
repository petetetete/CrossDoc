# Python Standard Library imports
import random
import time
import hashlib
import os

# Our module imports
from .store_helpers import *
from .logging import Logger

# The parsing uses parameter annotations to match command line arguments
# to the appropriate parameters (including aliases).

# Also, the parsing interprets the lack of a default value as a required
# parameter, while setting a default value to a list will return a list of
# command line arguments, and setting the default to any other value will
# simply take the first value the user gives


def project_init(name: "-name -n" = "Default CrossDoc Project Name",
                 stores: "-stores -s" = []) -> "init i":

  config = {
    "project_name": name,
    "stores": [os.path.normpath(s) for s in stores]
  }

  # Create config file
  create_config(config)

  # Create the requested stores
  for store in config["stores"]:
    create_store(os.path.basename(store), os.path.dirname(store))

  return CONFIG_NAME + " initialized in this directory"


def create_store(name: "-name -n" = "cdoc-store",
                 path: "-path -p" = os.getcwd()) -> "create-store cs":

  # Get full path from given info
  # TODO: Consider error checking here
  full_path = os.path.normpath(os.path.join(path, name))

  # If local, create directory
  if not os.path.exists(full_path):
    try:
      os.makedirs(full_path)
    except OSError:
      logger.fatal("unable to create directory")

  # Get current config settings and add store
  config = get_config()
  if (full_path not in [os.path.normpath(s) for s in config["stores"]]):
    config["stores"].append(full_path)

  # Update the config file
  create_config(config, True)

  return "store created at \"" + full_path + "\""


def generate_anchor() -> "generate-anchor ga g":

  hash_length = 16
  string_to_hash = str(time.time()) + "|" + str(random.uniform(0, 1))
  final_hash = hashlib.md5(string_to_hash.encode("utf-8")).hexdigest()

  return ANCHOR_HOOK + final_hash[:hash_length]


def create_comment(text: "-text -t",
                   store: "-store -st" = None,  # Referenced by index
                   anchor: "-anchor -a" = None,
                   set: "-set" = DEFAULT_SET) -> "create-comment cc c":

  # Determine the anchor to use
  curr_store = find_store(store)
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

  # Find the referenced comment
  file_path, anchor_json = find_comment(anchor, store)

  found_set = next((s for s in anchor_json if s["set"] == set), None)
  if found_set:
    return found_set["comment"]
  else:
    Logger.fatal("comment set not found")


def delete_comment(anchor: "-anchor -a",
                   store: "-store -s" = None,
                   set: "-set" = None) -> "delete-comment dc d":

  # Find the referenced comment
  file_path, anchor_json = find_comment(anchor, store)

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

  # Find the referenced comment
  file_path, anchor_json = find_comment(anchor, store)

  set_i = next((i for i, s in enumerate(anchor_json)
                if s["set"] == set), None)

  # Fail if not found
  if set_i is None:
    Logger.fatal("comment set not found")

  # Update set and update json
  anchor_json[set_i]["comment"] = text

  if not isinstance(file_path, tuple):  # Local
    with open(file_path, "w") as file:
      json.dump(anchor_json, file, indent=4, sort_keys=True)

  else:  # Remote

    # TODO: Authentication
    try:
      section_text = "=== " + set + " ===\n" + text
      wiki_request(file_path[0], action="edit", pageid=file_path[1],
                   section=anchor_json[set_i]["set_id"], token="+\\",
                   text=section_text)

    except Exception:
      Logger.fatal("unable to update remote source")

  return ("set \"" + anchor_json[set_i]["set"] + "\" at \"" +
          add_anchor_prefix(anchor) + "\" updated")


def hide_comments(files: "-files -f" = []) -> "hide-comments hc h":

  # TODO: Implement
  Logger.standard(files)
