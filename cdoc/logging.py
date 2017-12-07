# Python Standard Library imports
import sys
import os


class logger:

  def standard(message):
    """Logs a message to the user"""

    print(message)
    return

  def usage():
    """Logs the usage message for the function that called this"""

    # TODO: Look into the viability of this further (circular dependency issue)
    # previousFrame = inspect.currentframe().f_back
    # (_, _, functionName, _, _) = inspect.getframeinfo(previousFrame)
    # print(functionName)
    # print(registeredCommands[0].__name__)

    return

  def program(message):
    """Logs a message prefixed by the program name to the user"""

    name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    print(name + ": " + message)
    return

  def fatal(message):
    """Logs a fatal message to the user and kill the program"""

    print("fatal: " + message)
    sys.exit()
