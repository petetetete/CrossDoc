# Our module imports
from cdoc.example_functions import generateAnchor, fetchComment

# Array of registered command functions (make sure to import them to this file)
# The "primary" identifier should be placed first in the list
#
# Usage message delimeters:
#   ${identifier} -> will be replaced with the user-entered identifier
#
registeredCommands = [{
  "identifiers": ["generate-anchor", "ga", "g"],
  "function": generateAnchor,
  "usage": "${identifier}"
},
{
  "identifiers": ["fetch-comment", "fc", "f"],
  "function": fetchComment,
  "usage": "${identifier} <commentId>"
}]
