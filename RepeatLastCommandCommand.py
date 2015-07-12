import sublime, sublime_plugin

class RepeatLastCommandCommand(sublime_plugin.TextCommand):
  def run(self, edit, times = None):
    if times == None:
      self.ask_for_ttr()
    else:
      self.repeat_last_command(times)

  def on_done(self, times):
    try:
      ttr = int(times)
    except ValueError:
      message = str.format("Can’t repeat the last command ‘{0}’ times.\n\nPlease insert a number.", times)
      if sublime.ok_cancel_dialog(message):
        self.ask_for_ttr()
      return
    self.repeat_last_command(ttr)

  def ask_for_ttr(self):
    input_panel = self.view.window().show_input_panel('How many times ?', '', self.on_done, None, None)
    input_panel.settings().set('auto_insert_numbers', True)

  def repeat_last_command(self, times):
    command, args, _ = self.view.command_history(0, True)
    self.schedule_command(command, args, times)

  def schedule_command(self, command, args, times):
    sublime.set_timeout(lambda: self.run_command(command, args, times), 0)

  def run_command(self, command, args, times):
    self.view.run_command(command, args)
    if times > 1:
      self.schedule_command(command, args, times - 1)
