# Python Standard Library imports
import sys
import os
import inspect
from inspect import signature, Parameter

# Our module imports
import cdoc.registration


class Logger:

  def standard(message):
    """Logs a message to the user (non-ending)"""

    print(message)
    return

  def usage(command=None):
    """Logs the usage message for the function that called this (non-ending)"""

    name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    output = "usage: "

    # Find the function that wants its usage message printed
    if command is None:
      previousFrame = inspect.currentframe().f_back
      (_, _, functionName, _, _) = inspect.getframeinfo(previousFrame)

      usageCallee = next((a for a in cdoc.registration.commands
                          if a.__name__ == functionName), None)
    else:
      usageCallee = command

    # If we were called from within a command
    if usageCallee is not None:
      calleeSignature = signature(usageCallee)
      calleeParams = calleeSignature.parameters.items()

      output += name + " " + calleeSignature.return_annotation.split()[0] + " "

      for name, param in calleeParams:
        required = param.default == Parameter.empty
        takesList = isinstance(param.default, list)

        output += "[" if not required else ""
        output += param.annotation.split()[0] + " "
        output += "<list>" if takesList else "<value>"
        output += "] " if not required else " "

    # Print the default usage message
    else:
      commands = map((lambda a: signature(a).return_annotation.split()[0]),
                     cdoc.registration.commands)

      output += name + " <command>\n\nAll CrossDoc commands:\n  "
      output += "\n  ".join(commands)

    Logger.standard(output)
    return

  def program(message):
    """Logs a message prefixed by the program name to the user (non-ending)"""

    name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    Logger.standard(name + ": " + message)
    return

  def fatal(message):
    """Logs a fatal message to the user and kill the program (ending)"""

    Logger.standard("fatal: " + message)
    sys.exit()
