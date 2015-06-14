import sublime_plugin

class CloseAllInOtherGroupsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    window = self.view.window()
    groups = window.num_groups()
    active_group = window.active_group()

    for group in range(groups):
      if active_group != group:
        window.run_command("close_all_in_group", { "group": group })
