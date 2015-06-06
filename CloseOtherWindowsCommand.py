import sublime, sublime_plugin

class CloseOtherWindowsCommand(sublime_plugin.WindowCommand):
  def run(self):
    windows = sublime.windows()
    active_window = sublime.active_window()

    for window in sublime.windows():
      if active_window != window:
          window.run_command('close_window')
