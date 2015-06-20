import sublime, sublime_plugin

class RepeatLastCommandCommand(sublime_plugin.TextCommand):
  def run(self, edit, times = 1):
    command, args, _ = self.view.command_history(0, True)
    self.schedule_command(command, args, times)

  def schedule_command(self, command, args, times):
    sublime.set_timeout(lambda: self.run_command(command, args, times), 0)

  def run_command(self, command, args, times):
    self.view.run_command(command, args)
    if times > 1:
      self.schedule_command(command, args, times - 1)
