import math, sublime, sublime_plugin

class GotoBeginingOfViewportCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    x, y = self.view.viewport_position()
    line_height = self.view.line_height()
    lines = math.ceil(y / line_height)

    pos = self.view.layout_to_text((x, lines * line_height + line_height))

    self.view.sel().clear()
    self.view.sel().add(sublime.Region(pos, pos))
