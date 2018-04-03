# Python Standard Library imports
from inspect import signature, Parameter
from difflib import SequenceMatcher

# Our module imports
import cdoc.registration
from .logging import Logger

HELP_FLAGS = ["--h", "--help"]


# Processes the command line input and runs the appropriate function
def process_command(argv=[]):

  # They didn't give us anything
  if len(argv) == 1:
    Logger.usage()
    return

  identifier = argv[1]

  # They're looking for program level help text
  if len(argv) == 2 and identifier in HELP_FLAGS:
    Logger.usage()
    return

  # Find command requested in big list and run its associated function
  command = next((a for a in cdoc.registration.commands
                  if identifier in signature(a).return_annotation.split()),
                 None)

  # No valid command was found, let's provide a helpful message
  if command is None:
    output_similar_commands(identifier)
    return

  # Decode and save the temaining relevant arguments
  args = [bytes(x, "utf-8").decode("unicode_escape") for x in argv[2:]]

  # Print help text for the command if they've given us only a help flag
  if len(args) == 1 and args[0] in HELP_FLAGS:
    Logger.usage(command)
    return

  # Get command line argument information
  argsMap = {}
  for i in range(len(args)):

    # Skip past args that aren't a parameter (for now)
    if len(args[i]) == 0 or args[i][0] != '-' or args[i] in argsMap:
      continue

    # Initialize map element
    currList = argsMap[args[i]] = []

    while (i + 1 < len(args) and
           (len(args[i + 1]) == 0 or args[i + 1][0] != '-')):
      i += 1  # Increment iterator
      currList.append(args[i])  # Append parameter to current list

  finalParams = []
  requiredParams = signature(command).parameters.items()

  # Iterate through the command's parameters
  for name, param in requiredParams:
    required = param.default == Parameter.empty
    possibleArgs = param.annotation.split()

    matchingArg = next((b for a, b in argsMap.items()
                        if a in possibleArgs), None)

    # Parameter is required
    if required:
      # Case where the user has not provided ample info
      if matchingArg is None or matchingArg == []:
        Logger.usage(command)
        return
      else:
        finalParams.append(matchingArg[0])

    # Parameter is not required, and the user gave us something to work with
    elif matchingArg is not None:

      # Default expects many, pass along all the user gave us
      if isinstance(param.default, list):
        finalParams.append(matchingArg)

      # Defautl expects a boolean, set to true if the flag exists
      elif isinstance(param.default, bool):
        finalParams.append(True)

      # Default expects a single, and they gave it to us, so pass it along
      elif len(matchingArg) > 0:
        finalParams.append(matchingArg[0])

      else:  # User did not give us the requisite info
        finalParams.append(param.default)

    else:  # Parameter is not required and the user didn't give us anything
      finalParams.append(param.default)

  # Call the actual function with the users provided info
  output = command(*finalParams)
  if output is not None:
    Logger.standard(output)


# Used to determine if two strings are similar
def is_similar(a, b):
  return SequenceMatcher(None, a, b).ratio() >= 0.5


# Returns a list of tuples in which the first element is the command that
# is similar to the input, and the second element is the primary identifier
# of the command.
def find_similar_ids(id):

  similarIds = []
  for command in cdoc.registration.commands:
    identifiers = signature(command).return_annotation.split()
    newId = next((i for i in identifiers if is_similar(i, id)), None)
    if (newId is not None):
      mainId = identifiers[0]
      similarIds.append([newId, mainId if newId != mainId else None])

  return similarIds


def output_similar_commands(identifier):
  output = "'" + identifier + "' is not a command."

  # If there are any similar commands, add them to the output string
  similarIds = find_similar_ids(identifier)
  if (len(similarIds) > 0):
    output += "\n\nSimilar commands:"

    for id in similarIds[:3]:  # Only add up to 3 similar commands
      output += "\n  " + id[0]
      if (id[1] is not None):  # Append command main id (if it is necessary)
        output += " (" + id[1] + ")"

  Logger.program(output)
