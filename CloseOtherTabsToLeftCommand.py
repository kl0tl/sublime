import sublime_plugin

class CloseOtherTabsToLeftCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    window = self.view.window()
    group_index, view_index = window.get_view_index(self.view)

    for view in window.views():
      other_group_index, other_view_index = window.get_view_index(view)

      if other_group_index == group_index and other_view_index < view_index:
        view_index -= 1
        window.run_command("close_by_index", {
          "group": other_group_index,
          "index": other_view_index
        })
