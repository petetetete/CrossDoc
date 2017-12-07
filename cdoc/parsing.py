# Python Standard Library imports
from inspect import signature, Parameter
from difflib import SequenceMatcher
from pprint import pprint

# Our module imports
from .registered_commands import registeredCommands
from .logging import *


# Used to determine if two strings are similar
def isSimilar(a, b):
  return SequenceMatcher(None, a, b).ratio() >= 0.5


# Returns a list of tuples in which the first element is the command that
# is similar to the input, and the second element is the primary identifier
# of the command.
def findSimilarIds(id):

  similarIds = []
  for command in registeredCommands:
    newId = next((i for i in command["identifiers"] if isSimilar(i, id)), None)
    if (newId is not None):
      mainId = command["identifiers"][0]
      similarIds.append([newId, mainId if newId != mainId else None])

  return similarIds


def outputSimilarCommands(identifier):
  output = "'" + identifier + "' is not a command."

  # If there are any similar commands, add them to the output string
  similarIds = findSimilarIds(identifier)
  if (len(similarIds) > 0):
    output += "\nSimilar commands:"

    for id in similarIds[:3]:  # Only add up to 3 similar commands
      output += "\n  " + id[0]
      if (id[1] is not None):  # Append command main id (if it is necessary)
        output += " (" + id[1] + ")"

  logProgram(output)


# Processes the command line input and runs the appropriate function
def processCommand(argv):

  if len(argv) == 1:
    # TODO: Create usage message system
    logProgram("missing command")
    return

  identifier = argv[1]

  # Find command requested in big list and run its associated function
  command = next((x for x in registeredCommands
                  if identifier in x["identifiers"]), None)

  # No valid command was found, let's provide a helpful message
  if command is None:
    outputSimilarCommands(identifier)
    return

  # Get command line argument information
  argsMap = {}
  args = argv[2:]
  for i in range(len(args)):

    # Skip past args that aren't a parameter (for now)
    if args[i][0] != '-':
      continue

    # Initialize map element
    currList = argsMap[args[i]] = []

    while i + 1 < len(args) and args[i + 1][0] != '-':
      i += 1  # Increment iterator
      currList.append(args[i])  # Append parameter to current list

  finalParams = []
  requiredParams = signature(command["function"]).parameters

  for name, param in requiredParams.items():
    required = param.default == Parameter.empty
    possibleArgs = param.annotation.split()

    matchingArg = next((b for a, b in argsMap.items()
                        if a in possibleArgs), None)

    # TODO: Consider adding support for required array parameters
    # Currently, the options are 1 required, 1 not required, and * not required

    # Parameter is required
    if required:
      # Case where the user has not provided ample info
      if matchingArg is None or matchingArg == []:
        print("oops, they missed a param")
        sys.exit()
      else:
        finalParams.append(matchingArg[0])

    # Parameter is not required, and the user gave us something to work with
    elif matchingArg is not None:

      # Default expects many, pass along all the user gave us
      if isinstance(param.default, list):
        finalParams.append(matchingArg)

      # Default expects a single, and they gave it to us, so pass it along
      elif len(matchingArg) > 0:
        finalParams.append(matchingArg[0])

      else:  # User did not give us the requisite info
        finalParams.append(param.default)

    else:  # Parameter is not required and the user didn't give us anything
      finalParams.append(param.default)

  # Call the actual function with the users provided info
  command["function"](*finalParams)
