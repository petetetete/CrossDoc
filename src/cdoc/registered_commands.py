# Our module imports
from .example_commands import generateAnchor, fetchComment
from .commands import projectInit

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
  "identifiers": ["generate-anchor", "ga", "g"],
  "function": generateAnchor,
  "usage": "${identifier}"
}, {
  "identifiers": ["fetch-comment", "fc", "f"],
  "function": fetchComment,
  "usage": "${identifier} <commentId>"
}]
