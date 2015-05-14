import sublime, sublime_plugin

class ToggleColorSchemeCommand(sublime_plugin.TextCommand):

  def run(self, edit, **args):
    light_scheme = args["light"]
    dark_scheme  = args["dark"]

    settings = sublime.load_settings('Preferences.sublime-settings')
    current_scheme = settings.get('color_scheme')
    new_scheme = dark_scheme if (current_scheme == light_scheme) else light_scheme

    self.set(settings, new_scheme)

    sublime.save_settings('Preferences.sublime-settings')

  def set(self, settings, color_scheme):
    settings.set('color_scheme', color_scheme)
    for view in sublime.active_window().views():
        view.settings().set('color_scheme', color_scheme)
