import sublime_plugin

class CycleGroupCommand(sublime_plugin.WindowCommand):
  def run(self, forward=True):
    num_groups = self.window.num_groups() - 1
    active_group = self.window.active_group()
    next_group = active_group + (1 if forward else -1)

    if next_group > num_groups:
        next_group = 0
    elif (next_group < 0):
      next_group = num_groups

    self.window.focus_group(next_group)
