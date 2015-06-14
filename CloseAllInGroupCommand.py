import sublime_plugin

class CloseAllInGroupCommand(sublime_plugin.TextCommand):
  def run(self, edit, group):
    window = self.view.window()
    views = window.views_in_group(group)

    for view in views:
      group_index, view_index = window.get_view_index(view)
      window.run_command("close_by_index", {
        "group": group_index,
        "index": view_index
      })
