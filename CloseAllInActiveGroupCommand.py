import sublime_plugin

class CloseAllInActiveGroupCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    window = self.view.window()
    active_group = window.active_group()

    window.run_command("close_all_in_group", { "group": active_group })
