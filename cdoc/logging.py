# Python Standard Library imports
import sys
import os


def logStandard(message):
  """Logs a message to the user"""

  print(message)
  return


def logProgram(message):
  """Logs a message prefixed by the program name to the user"""
  name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
  print(name + ": " + message)
  return


def logFatal(message):
  """Logs a fatal message to the user and kill the program"""

  print("fatal: " + message)
  sys.exit()
