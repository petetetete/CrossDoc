# Python Standard Library imports
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
                  store: "-store -st" = None,  # Referenced by index
                  set: "-set" = None) -> "create-comment cc c":

  config = getConfig()
  if len(config["stores"]) == 0:
    logger.fatal("no comment stores to create to")

  # If we weren't given a specific store to save to
  if store is None:

    # Find first store that exists
    i = 0
    while i < len(config["stores"]) and not storeIsValid(config["stores"][i]):
      i += 1

    # We couldn't find a valid store
    if i >= len(config["stores"]):
      logger.fatal("no valid comment stores found")

    currStore = config["stores"][i]

  # We were given a store to check
  else:
    # TODO: Look into better store reference
    if (int(store) < len(config["stores"]) and
            storeIsValid(config["stores"][int(store)])):
      currStore = config["stores"][int(store)]
    else:
      currStore = ""
      logger.fatal("store specified is invalid")

  setToUse = DEFAULT_SET if set is None else set
  with open(currStore + "/" + setToUse + SET_EXTENSION, "a+") as file:
    anchor = generateAnchor()
    comment = anchor + "\n" + text + "\n\n"
    file.write(comment)

  return "comment created with anchor: " + anchor


def fetchComment(anchor: "-anchor -a",
                 store: "-store -s" = None) -> "fetch-comment fc f":

  try:
    filePath, start, end = findComment(anchor, store)
  except ValueError:
    logger.fatal("comment anchor not found")

  with open(filePath) as file:
    return "".join(file.readlines()[start + 1:end]).rstrip("\n")


def deleteComment(anchor: "-anchor -a",
                  store: "-store -s" = None) -> "delete-comment dc d":

  try:
    filePath, start, end = findComment(anchor, store)
  except ValueError:
    logger.fatal("comment anchor not found")

  with open(filePath, "r+") as file:
    lines = file.readlines()
    file.seek(0)
    file.writelines(lines[0:start] + lines[end:])
    file.truncate()

  return "comment at " + anchor + " deleted"


def updateComment(anchor: "-anchor -a",
                  text: "-text -t" = "",
                  store: "-store -s" = None) -> "update-comment uc u":

  try:
    filePath, start, end = findComment(anchor, store)
  except ValueError:
    logger.fatal("comment anchor not found")

  with open(filePath, "r+") as file:
    lines = file.readlines()
    file.seek(0)
    file.writelines(lines[0:start + 1] + [text + "\n", "\n"] + lines[end:])
    file.truncate()

  return "comment at " + anchor + " updated"
