import math, sublime, sublime_plugin

class GotoEndOfViewportCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    x, y = self.view.viewport_position()
    w, h = self.view.viewport_extent()
    line_height = self.view.line_height()
    lines = math.floor((y + h) / line_height)

    pos = self.view.layout_to_text((x, lines * line_height))

    self.view.sel().clear()
    self.view.sel().add(sublime.Region(pos, pos))
