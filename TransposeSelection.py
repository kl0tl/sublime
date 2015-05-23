import sublime, sublime_plugin

class TransposeSelectionCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    for region in self.view.sel():
      self.transpose_selection(region)

  def transpose_selection(self, region):
    self.view.sel().subtract(region)
    self.view.sel().add(sublime.Region(region.b, region.a))
