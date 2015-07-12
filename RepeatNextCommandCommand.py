import sublime, sublime_plugin

class RepeatNextCommandCommand(sublime_plugin.TextCommand):
  def run(self, edit, times = None):
    if times == None:
      self.ask_for_ttr()
    else:
      self.repeat_next_command(times)

  def on_done(self, times):
    try:
      ttr = int(times)
    except ValueError:
      message = str.format("Can’t repeat the next command ‘{0}’ times.\n\nPlease insert a number.", times)
      if sublime.ok_cancel_dialog(message):
        self.ask_for_ttr()
      return
    self.repeat_next_command(ttr)

  def ask_for_ttr(self):
    input_panel = self.view.window().show_input_panel('How many times ?', '', self.on_done, None, None)
    input_panel.settings().set('auto_insert_numbers', True)

  def repeat_next_command(self, times):
    settings = self.view.settings()
    settings.set('repeat_next_command', True)
    settings.set('repeat_next_command_times', times)
    self.view.set_status('repeat_next_command', '🔁' + str(times))


class RepeatNextCommandListener(sublime_plugin.EventListener):
  def on_text_command(self, view, command_name, args):
    settings = view.settings()
    repeat_next_command = settings.get('repeat_next_command')
    times = settings.get('repeat_next_command_times', 0)
    if repeat_next_command and times > 1:
      stop_repeat_next_command(view)
      self.schedule_command(view, command_name, args, times - 1)

  def schedule_command(self, view, command, args, times):
    sublime.set_timeout(lambda: self.run_command(view, command, args, times), 0)

  def run_command(self, view, command, args, times):
    view.run_command(command, args)
    if times > 1:
      self.schedule_command(view, command, args, times - 1)

class StopRepeatNextCommandCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    stop_repeat_next_command(self.view)

def stop_repeat_next_command(view):
  settings = view.settings()
  settings.set('repeat_next_command', False)
  settings.set('repeat_next_command_times', 0)
  view.erase_status('repeat_next_command')
