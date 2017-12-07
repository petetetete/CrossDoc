# Our module imports
from .commands import *

# Array of registered command functions (make sure to import them to this file)
# This registration API assumes that a command has:
#   return annotation -> denoting the possible aliases for the function
#   parameter annotations -> denoting the aliases of each parameter
#   parameter defaults -> denoting whether a param is required, and what type
#                         of input should be provided (<list> or <value>)
commands = [projectInit, createComment, generateAnchor,
            fetchComment, deleteComment]
