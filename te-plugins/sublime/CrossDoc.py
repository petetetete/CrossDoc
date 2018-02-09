import sublime
import sublime_plugin
from subprocess import check_output


class InsertCommentCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        v = self.view

        # Get line info
        line = v.line(v.sel()[0])
        line_text = v.substr(line)
        white_space = line_text[:len(line_text) - len(line_text.lstrip())]

        # Create and add comment to view
        anchor = check_output("cdoc generate-anchor",
                              shell=True).decode("utf-8").rstrip()
        string = white_space + anchor + "\n"
        v.insert(edit, line.begin(), string)

        # Move cursor to the end of the new comment
        v.sel().clear()
        v.sel().add(sublime.Region(line.begin() + len(string) - 1))

        # Toggle comment for the new string
        v.run_command("toggle_comment")

        print(check_output("cdoc generate-anchor", shell=True).rstrip())
