# Python Standard Library imports
import os
import random

# Our module imports
from .config_helpers import *
from .logging import logger

# The parsing uses parameter annotations to match command line arguments
# to the appropriate parameters (including aliases).

# Also, the parsing interprets the lack of a default value as a required
# parameter, while setting a default value to a list will return a list of
# command line arguments, and setting the default to any other value will
# simply take the first value the user gives


def projectInit(name: "-name -n" = "Default Project Name",
                stores: "-stores -s" = []) -> "init i":

  config = {
    "project_name": name,
    "stores": stores
  }

  try:
    createConfig(config)
  except FileExistsError:
    logger.fatal("configuration file already exists")

  return CONFIG_NAME + " initialized in this directory"


def generateAnchor() -> "generate-anchor ga g":
  return ANCHOR_HOOK + str(random.getrandbits(24))


def createComment(text: "-text -t",
                  store: "-store -st" = "",  # TODO: Alias stores
                  set: "-set" = "") -> "create-comment cc c":

  config = getConfig()
  if len(config["stores"]) == 0:
    logger.fatal("no comment stores to create to")

  # If we weren't given a specific store to save to
  if store == "":

    # Find first store that exists
    i = 0
    while i < len(config["stores"]) and not os.path.isdir(config["stores"][i]):
      i += 1

    # We couldn't find a valid store
    if i >= len(config["stores"]):
      logger.fatal("no valid comment stores found")

    currStore = config["stores"][i]

  # We were given a store to check
  else:
    currStore = ""
    logger.fatal("store specification not yet supported")

  if set == "":
    with open(currStore + "/" + DEFAULT_SET + SET_EXTENSION, "a+") as file:
      # TODO: Replace with generateAnchor
      # TODO: Create better comment storage format (that's simple)
      anchor = generateAnchor()
      comment = anchor + "\n" + text + "\n\n"
      file.write(comment)

  # TODO: user specified a set
  else:
    logger.fatal("set specification not yet supported")

  return "comment created with anchor: " + anchor


def fetchComment(anchor: "-anchor -a",
                 store: "-store -s" = None) -> "fetch-comment fc f":

  try:
    filePath, start, end = findComment(anchor, store)
  except ValueError:
    logger.fatal("comment anchor not found")

  with open(filePath) as file:
    return "".join(file.readlines()[start + 1:end]).rstrip("\n")
