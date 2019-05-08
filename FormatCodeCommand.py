import os
import sublime
import sublime_plugin
import subprocess

def decode_bytes(src, encoding):
    return src.decode(encoding).replace("\r\n", "\n").replace("\r", "\n")

def encode_bytes(src, encoding):
    return src.replace("\r\n", os.linesep).replace("\n", os.linesep).encode(encoding)

def load_view_settings(view):
  return load_syntax_settings(view.settings().get("syntax"))

def load_syntax_settings(syntax):
  return sublime.load_settings(os.path.splitext(os.path.basename(syntax))[0] + ".sublime-settings")

class FormatCodeCommand(sublime_plugin.TextCommand):
  def run(self, edit, name = None):
    window = self.view.window()
    syntax = self.view.settings().get("syntax")
    settings = load_syntax_settings(syntax)
    formatter = settings.get("format_code")
    if not formatter :
      window.status_message("No formatter for syntax '%s'" % syntax)
      return
    if not formatter.get("enabled", True):
      window.status_message("Formatter disabled for syntax '%s'" % syntax)
      return
    main = formatter.get("executable")
    if name is None and main:
      self.format(edit, main, formatter.get("paths"))
      return
    else:
      exes = formatter.get("executables")
      cmd = next((exe["cmd"] for exe in exes if exe["name"] == name), None)
      if cmd is None:
        if len(exes) == 1:
          self.format(edit, exes[0]["cmd"], formatter.get("paths"))
          return
        else:
          self.view.window().show_quick_panel([exe["cmd"] for exe in exes], self.on_quick_choice(formatter))
          return
      else:
        self.format(edit, cmd, formatter.get("paths"))
        return
    window.status_message("Missing formatter commands for syntax '%s'" % syntax)

  def on_quick_choice(self, formatter):
    def callback(index):
      if index > -1:
        self.view.run_command("format_code", { "name": formatter["executables"][index]["name"] })
    return callback

  def format(self, edit, cmd, paths = None):
    regions = list(self.view.sel())
    if all([region.empty() for region in regions]):
      self.format_region(edit, sublime.Region(0, self.view.size()), cmd, paths)
    else:
      for region in regions:
        self.format_region(edit, region, cmd, paths, trailing_newline = False)
    self.view.sel().clear()
    self.view.sel().add_all(regions)

  def format_region(self, edit, region, cmd, paths = None, trailing_newline = True):
    encoding = self.view.encoding()
    if encoding == "Undefined":
      encoding = self.view.settings().get("default_encoding")
    env = dict(os.environ)
    if paths and sublime.platform() in paths:
      env["PATH"] = os.pathsep.join(paths[sublime.platform()]) + os.pathsep + env.get("PATH", "")
    if self.view.file_name():
      cwd = os.path.dirname(self.view.file_name())
    else:
      cwd = env["HOME"]
    proc = subprocess.Popen([cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, cwd=cwd, shell=True)
    try:
      raw = self.view.substr(region)
      stdout, stderr = proc.communicate(encode_bytes(raw, encoding))
      proc.wait()
      if stderr:
        sublime.status_message(decode_bytes(stderr, encoding))
      elif stdout:
        formatted = decode_bytes(stdout if trailing_newline else stdout.rstrip(), encoding)
        if raw != formatted:
          self.view.replace(edit, region, formatted)
    finally:
      proc.stdin.close()
      proc.stdout.close()
      proc.stderr.close()

class FormatCodeOnSave(sublime_plugin.ViewEventListener):
  def on_pre_save(self):
    settings = load_view_settings(self.view)
    formatter = settings.get("format_code")
    if formatter and formatter.get("enabled", True) and formatter.get("enabled_on_save", True):
      if formatter.get("executable"):
        self.view.run_command("format_code")
      else:
        exes = formatter.get("executables")
        default = next((exe["name"] for exe in exes if exe["name"] == formatter.get("default")), None)
        if default:
          self.view.run_command("format_code", { "name": default })
