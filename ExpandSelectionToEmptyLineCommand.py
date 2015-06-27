import sublime, sublime_plugin

class ExpandSelectionToEmptyLineCommand(sublime_plugin.TextCommand):
  def run(self, edit, forward=True):
    regions = self.view.sel()
    for region in regions:
      print(region)
      if forward:
        end = self.view.find_by_class(region.end(), True, sublime.CLASS_EMPTY_LINE)
        new_region = sublime.Region(region.begin(), end)
      else:
        start = self.view.find_by_class(region.begin(), False, sublime.CLASS_EMPTY_LINE)
        new_region = sublime.Region(region.end(), start)
      regions.subtract(region)
      regions.add(new_region)
