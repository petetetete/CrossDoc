# Python Standard Library imports
from pprint import pprint

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

  logger.standard(CONFIG_NAME + " initialized in this directory")
  return


def createComment(text: "-text -t",
                  store: "-store -st" = "",  # TODO: Alias stores
                  set: "-set" = "") -> "create-comment cc c":

  # TODO: Move somwhere better
  DEFAULT_SET = "No Set"
  SET_EXTENSION = ".txt"

  pprint(getConfig())

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
    print(config["stores"][i])

  # We were given a store to check
  else:
    currStore = ""
    logger.fatal("store specification not yet supported [TODO]")

  if set == "":
    with open(currStore + "/" + DEFAULT_SET + SET_EXTENSION, "a+") as file:
      # TODO: Replace with generateAnchor
      # TODO: Create better comment storage format (that's simple)
      comment = "<&> 123456anchorhere123456\n" + text + "\n\n"
      file.write(comment)

  return
