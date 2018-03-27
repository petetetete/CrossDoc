import sublime
import sublime_plugin
from subprocess import check_output
import os

ANCHOR_HOOK = "<&> "


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
    line_text = v.substr(line)
    white_space = line_text[:len(line_text) - len(line_text.lstrip())]

    # Get current working directory
    cwd = os.path.dirname(v.file_name())

    # Create and add comment to view
    output = check_output("cdoc cc -t \"[COMMENT TEXT]\"",
                          shell=True, cwd=cwd).decode("utf-8").rstrip()

    # Catch command line errors
    if output.startswith("fatal"):
      print(output)
      return

    # Split output line by carriage return
    output_lines = [white_space + l + "\n" for l in output.split("\r\n")]

    # Insert created comment to file
    v.insert(edit, line.begin(), "".join(output_lines))

    # Clear all cursors and save the line beginning
    v.sel().clear()
    char_point = line.begin()

    # For each line added to the file, add a cursor
    for output_line in output_lines:
      v.sel().add(sublime.Region(char_point))
      char_point += len(output_line)

    # Toggle comment for the new string
    v.run_command("toggle_comment")

    # Clear all cursors and reset the cursor to the end of the new comment
    last_cursor = v.sel()[-1]
    v.sel().clear()
    v.sel().add(sublime.Region(v.full_line(last_cursor).b - 1))


class DeleteCommentCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    v = self.view

    # Get line info
    line = v.line(v.sel()[0])

    # Catch attempting to use the delete while not selecting a comment
    if not v.match_selector(line.end(), "comment"):
      print("fatal: not selecting a comment")
      return

    # Find the CrossDoc hook region
    h_region = line
    while (v.match_selector(h_region.end(), "comment") and
           ANCHOR_HOOK not in v.substr(h_region)):
      h_region = v.line(h_region.begin() - 1)

    # If we ran out of comment before finding an anchor
    if ANCHOR_HOOK not in v.substr(h_region):
      print("fatal: cannot find anchor")
      return

    # Save the line's text
    h_line_text = v.substr(h_region)

    # Try to get the anchor and set from the line
    try:
      anchor = getAnchorFromLine(h_line_text)
      # TODO: set = getSetFromLine(h_line_text)

    # Catch maniuplated hook lines
    except ValueError:
      print("fatal: cannot find anchor")
      return

    # Get current working directory and run delete
    cwd = os.path.dirname(v.file_name())
    output = check_output("cdoc dc -a " + anchor,
                          shell=True, cwd=cwd).decode("utf-8").rstrip()

    # Catch command line errors
    if output.startswith("fatal"):
      print(output)
      return

    # Find the start and end of the comment region
    c_region_start = h_region.begin()
    while v.match_selector(h_region.end(), "comment"):
      h_region = v.line(h_region.end() + 1)
    c_region_end = h_region.begin()

    # Remove the comment from the actual file
    v.erase(edit, sublime.Region(c_region_start, c_region_end))


class UpdateCommentsCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    v = self.view

    # Get Sublime regions of all lines, comments, and CrossDoc hooks
    l_regions = v.split_by_newlines(sublime.Region(0, v.size()))
    c_regions = [x for x in l_regions if v.match_selector(x.end(), "comment")]
    h_regions = [x for x in c_regions if ANCHOR_HOOK in v.substr(x)]

    # For all CrossDoc hook regions
    for h_region in h_regions:

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

      # Get current working directory and run update
      cwd = os.path.dirname(v.file_name())
      output = check_output("cdoc uc -a " + anchor + " -t \"" +
                            text + "\" -set \"" + set + "\"",
                            shell=True, cwd=cwd).decode("utf-8").rstrip()

      # Catch command line errors
      if output.startswith("fatal"):
        print("warning: unable to update comment at line", h_line_num)
        return


# Event listener callbacks

class UpdateOnSave(sublime_plugin.EventListener):

  def on_post_save_async(self, v):
    v.run_command("update_comments")


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
