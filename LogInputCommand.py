import sublime, sublime_plugin

class LogInputCommand(sublime_plugin.TextCommand):
  def run(self, edit, value = True):
    sublime.log_input(value)
    sublime.status_message('Log inputs' if value else 'Stop logging inputs')
