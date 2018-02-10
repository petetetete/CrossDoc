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

        # Start finding the anchor
        split_line = line_text.split(" ")
        anchor_index = split_line.index(ANCHOR_HOOK.strip()) + 1

        # Catch invalid anchor errors
        if anchor_index >= len(split_line):
            print("fatal: cannot find anchor")
            return

        # Save the found anchor
        anchor = split_line[anchor_index]

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
