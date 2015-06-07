import sublime_plugin

class GotoMarkCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    regions = self.view.get_regions('mark')

    if len(regions) > 0:
      sel = self.view.sel()
      mark = regions[0]

      sel.clear()
      sel.add(mark)
      self.view.show_at_center(mark)
