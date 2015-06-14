import sublime_plugin

class ResetLayoutCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    window = self.view.window()
    window.run_command("set_layout", {
      "cols": [0.0, 1.0],
      "rows": [0.0, 1.0],
      "cells": [[0, 0, 1, 1]]
    })
