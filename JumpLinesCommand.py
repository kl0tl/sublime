import sublime, sublime_plugin

class JumpLinesCommand(sublime_plugin.TextCommand):
  def run(self, edit, number_of_lines = None, forward = True, extend = False):
    if number_of_lines == None:
      self.ask_for_number_of_lines(forward, extend)
    else:
      self.jump_lines(number_of_lines, forward, extend)

  def ask_for_number_of_lines(self, forward, extend):
    callback = lambda value: self.on_done(value, forward, extend)
    input_panel = self.view.window().show_input_panel('How many lines ?', '', callback, None, None)
    input_panel.settings().set('auto_insert_numbers', True)

  def on_done(self, value, forward, extend):
    try:
      number_of_lines = int(value)
    except ValueError:
      message = str.format('Can’t jump ‘{0}’ lines.\n\nPlease insert a number.', value)
      if sublime.ok_cancel_dialog(message):
          self.ask_for_number_of_lines(forward, extend)
          return
    self.jump_lines(number_of_lines, forward, extend)

  def jump_lines(self, number_of_lines, forward, extend):
    if number_of_lines < 0:
      forward = not forward
    for _ in range(abs(number_of_lines)):
      self.view.run_command('move', { 'by': 'lines', 'forward': forward, 'extend': extend })
