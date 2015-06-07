import os, sublime, sublime_plugin

class CopyFolderPathCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    file_name = self.view.file_name()
    if file_name:
      dir_name = os.path.dirname(file_name)
      sublime.set_clipboard(dir_name)
