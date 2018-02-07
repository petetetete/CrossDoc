import sublime
import sublime_plugin


class InsertCommentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        v = self.view

        first_cursor = v.sel()[0]
        curr_line = v.line(first_cursor)

        # Toggle the comment for the
        v.run_command("toggle_comment")
        self.view.insert(edit, curr_line.a + 2,
                         "<&> ANCHOR: Example comment \n")
