# Imports
from example_functions import *
from inspect import signature


# TODO: Consider moving this to its own file, command_registration.py (?)
# Array of registered command functions (make sure to import them to this file)
commands = [{
  "identifiers": ["generate-anchor", "ga", "g"],
  "function": generateAnchor,
  "help": "This is the help message associated with generate anchor..."
},
{
  "identifiers": ["fetch-comment", "fc", "f"],
  "function": fetchComment
}]


# Processes the command line input
def processCommand(argv):

  if len(argv) == 1:
    print("Help text here... (Missing a command)")
    return

  # Find command requested in big list and run its associated function
  command = next((x for x in commands if argv[1] in x["identifiers"]), None)

  # In the case we found a matching command
  if command != None:

    remainingArgs = argv[2:] # Remaining relevant arguments

    commandSig = signature(command["function"])
    commandNumArgs = len(commandSig.parameters)

    # TODO: Handle defaulted arguments better
    # TODO: Think of method to handle flags
    # If the number of given arguments exceeds, just pass the needed ones
    if (len(remainingArgs) >= commandNumArgs):
      command["function"](*remainingArgs[0:commandNumArgs])
    else:

      if ("help" in command): # Print the commands help text (if it exists)
        print(command["help"])
      else:
        print("Default invalid number of arguments message here...")


  else:
    print("No valid command message here...")

  return
