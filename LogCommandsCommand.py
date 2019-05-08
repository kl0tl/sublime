import sublime, sublime_plugin

class LogCommandsCommand(sublime_plugin.TextCommand):
  def run(self, edit, value = True):
    sublime.log_commands(value)
    sublime.status_message('Log commands' if value else 'Stop logging commands')
