import sublime
import sublime_plugin
from subprocess import check_output
import os

ANCHOR_HOOK = "<&> "


class InsertCommentCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    v = self.view

    # Get line info
    line = v.full_line(v.sel()[0])
    line_text = v.substr(line)
    white_space = line_text[:len(line_text) - len(line_text.lstrip())]

    # Get current working directory
    cwd = os.path.dirname(v.file_name())

    # Create and add comment to view
    output = check_output("cdoc create-comment -text \"[COMMENT TEXT]\"",
                          shell=True, cwd=cwd).decode("utf-8").rstrip()

    # Catch command line errors
    if output.startswith("fatal"):
      print(output)
      return

    # Insert created comment to file
    string = white_space + output + "\n"
    v.insert(edit, line.begin(), string)

    # Move cursor to the end of the new comment
    v.sel().clear()
    v.sel().add(sublime.Region(line.begin() + len(string) - 1))

    # Toggle comment for the new string
    v.run_command("toggle_comment")


class DeleteCommentCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    v = self.view

    # Get line info
    line = v.full_line(v.sel()[0])
    line_text = v.substr(line)

    # Catch attempting to use the delete while not selecting a comment
    if ANCHOR_HOOK not in line_text:
      print("fatal: not selecting a comment")
      return

    # Find the anchor on the current line
    try:
      anchor = getAnchorFromLine(line_text)

    except ValueError:
      print("fatal: cannot find anchor")
      return

    # Get current working directory and run delete
    cwd = os.path.dirname(v.file_name())
    output = check_output("cdoc delete-comment -a " + anchor,
                          shell=True, cwd=cwd).decode("utf-8").rstrip()

    # Catch command line errors
    if output.startswith("fatal"):
      print(anchor)
      return

    # Clear the line in the file
    v.erase(edit, line)


class UpdateOnSave(sublime_plugin.EventListener):

  def on_post_save_async(self, v):

    # Get current file contents
    file_contents = v.substr(sublime.Region(0, v.size()))

    # Ensure that a hook even exists before continuing
    if ANCHOR_HOOK in file_contents:

      # Find the lines with the anchors
      file_lines = file_contents.split("\n")
      anchor_lines = [line for line in file_lines if ANCHOR_HOOK in line]

      # Iterate over found lines
      for line in anchor_lines:

        # Save the current line number
        line_num = file_lines.index(line) + 1

        # Try to find the anchor and comment text
        try:
          anchor = getAnchorFromLine(line)
          text = getCommentFromLine(line)
        except ValueError:
          print("warning: invalid anchor skipped at line", line_num)
          continue

        # Get current working directory and run update
        cwd = os.path.dirname(v.file_name())
        output = check_output("cdoc uc -a " + anchor + " -t \"" + text + "\"",
                              shell=True, cwd=cwd).decode("utf-8").rstrip()

        # Catch command line errors
        if output.startswith("fatal"):
          print("warning: unable to update comment at line", line_num)
          return


# Helper Methods #

def getAnchorFromLine(line):
  """Gets anchor from a line string

  Raises:
    ValueError: Cannot find anchor hook"""

  # Divide line
  split_line = line.split(" ")

  # Try to find the anchor in the line
  try:
    anchor_index = split_line.index(ANCHOR_HOOK.strip()) + 1

    if anchor_index >= len(split_line):
      raise ValueError

  # Catch invalid anchor errors
  except ValueError:
    raise ValueError("Cannot find anchor hook")

  # Return the found anchor
  return split_line[anchor_index]


def getCommentFromLine(line):
  """Gets comment from a line string"""

  # Divide line
  split_line = line.split(" ")
  comment = ""

  # Try to find the comment in the line
  try:
    comment_index = split_line.index(ANCHOR_HOOK.strip()) + 2

    if comment_index < len(split_line):
      comment = " ".join(split_line[comment_index:])

  except ValueError:
    pass

  # Return the found comment or default
  return comment
