import os, sublime, sublime_plugin, subprocess

def open(args):
  try:
    subprocess.Popen(args, cwd = os.path.join(sublime.packages_path(), 'User'))
  except (Exception) as exception:
    sublime.error_message('Open Terminal: ' + str(exception))

def locate_view(view):
  syntax = view.settings().get('syntax')
  if syntax == 'Packages/FileBrowser/dired.hidden-tmLanguage':
    return view.settings().get('dired_path')
  else:
    file_name = view.file_name()
    if file_name:
      return os.path.dirname(file_name)
    else:
      raise Exception('Can’t locate this buffer.')

class OpenTerminalCommand(sublime_plugin.WindowCommand):
  def run(self):
    try:
      self.open()
    except (Exception) as exception:
      sublime.error_message('OpenTerminal: ' + str(exception))

class OpenTerminalTabCommand(OpenTerminalCommand):
  def open(self):
    open(['./OpenTerminalTab', locate_view(self.window.active_view())])

class OpenTerminalWindowCommand(OpenTerminalCommand):
  def open(self):
    open(['./OpenTerminalWindow', locate_view(self.window.active_view())])

def locate_project(window):
  folders = window.folders()
  if len(folders) == 0:
    raise Exception('Can’t locate any project.')
  else:
    return folders[0]

class OpenTerminalTabAtProjectRootCommand(OpenTerminalCommand):
  def open(self):
    open(['./OpenTerminalTab', locate_project(self.window)])

class OpenTerminalWindowAtProjectRootCommand(OpenTerminalCommand):
  def open(self):
    open(['./OpenTerminalWindow', locate_project(self.window)])
