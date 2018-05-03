import sublime
import sublime_plugin
from subprocess import check_output
from time import time
import os

ANCHOR_HOOK = "<&> "
last_saved = time() * 1000


class InitCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    v = self.view

    # Get current working directory
    cwd = os.path.dirname(v.file_name())

    # Initialize repository in the cwd
    output = check_output("cdoc init",
                          shell=True, cwd=cwd).decode("utf-8").rstrip()

    # Catch command line errors
    if output.startswith("fatal"):
      print(output)
      return


class InsertCommentCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    v = self.view

    # Get line info
    line = v.full_line(v.sel()[0])

    # Get current working directory
    cwd = os.path.dirname(v.file_name())

    # Create and add comment to view
    output = check_output("cdoc cc -t \"[COMMENT TEXT]\"",
                          shell=True, cwd=cwd).decode("utf-8").rstrip()

    # Catch command line errors
    if output.startswith("fatal"):
      print(output)
      return

    # Insert comment in to file
    insertComment(edit, v, line, output)


class DeleteCommentCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    v = self.view

    # Get comment info
    h_region, anchor, set = getCommentInfo(edit, v)
    if h_region is None:
      return

    # Get current working directory and run delete
    cwd = os.path.dirname(v.file_name())
    output = check_output("cdoc dc -a " + anchor,
                          shell=True, cwd=cwd).decode("utf-8").rstrip()

    # Catch command line errors
    if output.startswith("fatal"):
      print(output)
      return

    # Delete comment
    deleteComment(edit, v, h_region)


class UpdateCommentsCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    v = self.view

    # Get Sublime regions of all lines, comments, and CrossDoc hooks
    l_regions = v.split_by_newlines(sublime.Region(0, v.size()))
    c_regions = [x for x in l_regions if v.match_selector(x.end(), "comment")]
    h_regions = [x for x in c_regions if ANCHOR_HOOK in v.substr(x)]

    # For all CrossDoc hook regions
    for h_region in reversed(h_regions):

      # Save the current hook regions line number and line text
      h_line_num = l_regions.index(h_region) + 1
      h_line_text = v.substr(h_region)

      # Try to get the anchor and set from the line
      try:
        anchor = getAnchorFromLine(h_line_text)
        set = getSetFromLine(h_line_text)

      # Catch maniuplated hook lines
      except ValueError:
        print("warning: invalid anchor/set skipped at line", h_line_num)
        continue

      # Save the comment region beyond the hook
      c_region_i = c_regions.index(h_region) + 1
      t_regions = []

      # Save all consecutive comment regions as text regions
      while c_regions[c_region_i - 1].b + 1 == c_regions[c_region_i].a:
        t_regions.append(c_regions[c_region_i])
        c_region_i += 1

      # Get the text from the text regions
      text = "\\n".join([
        " ".join(v.substr(x).lstrip().split(" ")[1:]) for x in t_regions
      ])

      global last_saved

      # Get current working directory and run update
      cwd = os.path.dirname(v.file_name())
      output = check_output("cdoc uc -a " + anchor + " -t \"" + text +
                            "\" -set \"" + set + "\"" + " -time \"" +
                            str(last_saved) + "\"",
                            shell=True, cwd=cwd).decode("utf-8").rstrip()

      # Catch command line errors
      if output.startswith("fatal"):
        print("warning: unable to update comment at line", h_line_num)
        return

      # Delete existing comment
      deleteComment(edit, v, h_region)

      # Insert comment in to file
      insertComment(edit, v, h_region, output)

    last_saved = time() * 1000


class NextSetCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    v = self.view

    # Get comment info
    h_region, anchor, set = getCommentInfo(edit, v)

    # Get current working directory and run delete
    cwd = os.path.dirname(v.file_name())
    output = check_output("cdoc fc -a " + anchor + " -set \"" + set + "\" --ns",
                          shell=True, cwd=cwd).decode("utf-8").rstrip()

    # Catch command line errors
    if output.startswith("fatal"):
      print(output)
      return

    # Delete existing comment
    deleteComment(edit, v, h_region)

    # Insert comment in to file
    insertComment(edit, v, v.line(v.sel()[0]), output)


class PrevSetCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    v = self.view

    # Get comment info
    h_region, anchor, set = getCommentInfo(edit, v)

    # Get current working directory and run delete
    cwd = os.path.dirname(v.file_name())
    output = check_output("cdoc fc -a " + anchor + " -set \"" + set + "\" --ps",
                          shell=True, cwd=cwd).decode("utf-8").rstrip()

    # Catch command line errors
    if output.startswith("fatal"):
      print(output)
      return

    # Delete existing comment
    deleteComment(edit, v, h_region)

    # Insert comment in to file
    insertComment(edit, v, v.line(v.sel()[0]), output)


# Event listener callbacks

class UpdateOnSave(sublime_plugin.EventListener):

  def on_pre_save(self, v):
    v.run_command("update_comments")


# Helper Methods #

def getCommentInfo(edit, v):

  # Get line info
  line = v.line(v.sel()[0])

  # Catch attempting to use the delete while not selecting a comment
  if not v.match_selector(line.end(), "comment"):
    print("fatal: not selecting a comment")
    return None, None, None

  # Find the CrossDoc hook region
  h_region = line
  while (v.match_selector(h_region.end(), "comment") and
         ANCHOR_HOOK not in v.substr(h_region)):
    h_region = v.line(h_region.begin() - 1)

  # If we ran out of comment before finding an anchor
  if ANCHOR_HOOK not in v.substr(h_region):
    print("fatal: cannot find anchor")
    return None, None, None

  # Save the line's text
  h_line_text = v.substr(h_region)

  # Try to get the anchor and set from the line
  try:
    anchor = getAnchorFromLine(h_line_text)
    set = getSetFromLine(h_line_text)

  # Catch maniuplated hook lines
  except ValueError:
    print("fatal: cannot find anchor")
    return None, None, None

  return h_region, anchor, set


def insertComment(edit, v, line, comment):

  line_text = v.substr(line)
  white_space = line_text[:len(line_text) - len(line_text.lstrip())]

  # Split output line by carriage return
  comment_lines = [white_space + l + "\n" for l in comment.split("\r\n")]

  # Insert created comment to file
  v.insert(edit, line.begin(), "".join(comment_lines))

  # Clear all cursors and save the line beginning
  v.sel().clear()
  char_point = line.begin()

  # For each line added to the file, add a cursor
  for comment_line in comment_lines:
    v.sel().add(sublime.Region(char_point))
    char_point += len(comment_line)

  # Toggle comment for the new string
  v.run_command("toggle_comment")

  # Clear all cursors and reset the cursor to the end of the new comment
  last_cursor = v.sel()[-1]
  v.sel().clear()
  v.sel().add(sublime.Region(v.full_line(last_cursor).b - 1))


def deleteComment(edit, v, line):

  # Find the start and end of the comment region
  c_region_start = line.begin()
  while v.match_selector(line.end(), "comment"):
    line = v.line(line.end() + 1)
  c_region_end = line.begin()

  # Remove the comment from the actual file
  v.erase(edit, sublime.Region(c_region_start, c_region_end))


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


def getSetFromLine(line):
  """Gets set name from a line string

  Raises:
    ValueError: Cannot find set name hook"""

  # Divide line
  split_line = line.replace("[", "").replace("]", "").split(" ")

  # Try to find the anchor in the line
  try:
    set_index = split_line.index(ANCHOR_HOOK.strip()) + 2

    if set_index >= len(split_line):
      raise ValueError

  # Catch invalid anchor errors
  except ValueError:
    raise ValueError("Cannot find anchor hook")

  # Return the found anchor
  return " ".join(split_line[set_index:])
