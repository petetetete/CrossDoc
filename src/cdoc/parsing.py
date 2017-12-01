# Python Standard Library imports
import os
from inspect import signature
from difflib import SequenceMatcher

# Our module imports
from cdoc.registered_commands import registeredCommands


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
    if (newId != None):
      mainId = command["identifiers"][0]
      similarIds.append([newId, mainId if newId != mainId else None])

  return similarIds


# Processes the command line input and runs the appropriate function
def processCommand(argv):

  if len(argv) == 1:
    print("Help text here... (Missing a command)")
    return

  progName = os.path.splitext(os.path.basename(argv[0]))[0]
  identifier = argv[1]

  # Find command requested in big list and run its associated function
  command = next(
    (x for x in registeredCommands if identifier in x["identifiers"]), None)

  # In the case we found a matching command
  if command != None:

    remainingArgs = argv[2:] # Remaining relevant arguments

    commandSig = signature(command["function"])
    commandNumArgs = len(commandSig.parameters)

    # TODO: Handle defaulted arguments better
    # TODO: Think of method to handle flags

    # If the number of given arguments exceeds, just pass the needed ones
    if (len(remainingArgs) >= commandNumArgs):
      command["function"](*remainingArgs[:commandNumArgs])
    else:

      if ("usage" in command): # Print the command's help text (if it exists)
        message = command["usage"].replace("${identifier}", identifier)
        print("usage:", message)
      else:
        print("Default invalid number of arguments message here...")


  # No valid command was found, let's provide a helpful message
  else:
    output = progName + ": '" + identifier + "' is not a command.\n"

    # If there are any similar commands, add them to the output string
    similarIds = findSimilarIds(identifier)
    if (len(similarIds) > 0):
      output += "\nSimilar commands:"

      for id in similarIds[:3]: # Only add up to 3 similar commands
        output += "\n  " + id[0]
        if (id[1] != None): # Append command main id (if it is necessary)
          output += " (" + id[1] + ")"

    print(output)
