# Our module imports
from .commands import projectInit, createComment

# Array of registered command functions (make sure to import them to this file)
# The "primary" identifier should be placed first in the list
#
# Usage message delimeters:
#   ${identifier} -> will be replaced with the user-entered identifier
#
registeredCommands = [{
  "identifiers": ["init", "i"],
  "function": projectInit,
  "usage": "${identifier}"
}, {
  "identifiers": ["create-comment", "cc", "c"],
  "function": createComment,
  "usage": "${identifier}"
}]
