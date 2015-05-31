import sublime_plugin


class CycleGroupCommand(sublime_plugin.TextCommand):
  def run(self, edit, forward=True):
    num_groups = self.view.window().num_groups() - 1
    active_group = self.view.window().active_group()
    next_group = active_group + (1 if forward else -1)

    if next_group > num_groups:
        next_group = 0
    elif (next_group < 0):
      next_group = num_groups

    self.view.window().focus_group(next_group)
