import sys

# Example function to be referenced in command
def testFunction():
  print("test");


# Array of each program command
commands = [{
  "identifiers": ["commit", "c"],
  "function": testFunction
}]

# Example CLI parse function
def parseCommand():

  # Catch case with no parameters
  if len(sys.argv) == 1:
    print("Help text here")
    return

  # Find command requested in big list and run its associated function
  command = next((x for x in commands if sys.argv[1] in x["identifiers"]), None)

  if command != None:
    command["function"]()
  else:
    print("Some text about an invalid command here")


# "Main" function
if __name__ == "__main__":
  parseCommand();
