import sublime, sublime_plugin

def update_settings(path, key, value):
  sublime.load_settings(path).set(key, value)
  sublime.save_settings(path)

class ToggleColorSchemesCommand(sublime_plugin.WindowCommand):
  def run(self, themes, color_schemes):
    settings = sublime.load_settings('Preferences.sublime-settings')

    light_theme = themes['light']
    dark_theme = themes['dark']

    was_dark_theme = settings.get('theme', light_theme) == dark_theme

    new_theme = light_theme if was_dark_theme else dark_theme
    update_settings('Preferences.sublime-settings', 'theme', new_theme)

    for color_scheme in color_schemes:
      new_scheme = color_scheme.get('light' if was_dark_theme else 'dark')
      update_settings(color_scheme.get('settings'), 'color_scheme', new_scheme)

    for view in self.window.views():
        best_score = -1
        best_candidate = None

        for color_scheme in color_schemes:
          for scope in color_scheme.get('scopes', []):
            score = view.score_selector(0, scope)
            if score > best_score:
              best_score = score
              best_candidate = color_scheme

        if best_candidate:
          new_scheme = best_candidate.get('light' if was_dark_theme else 'dark')
          view.settings().set('color_scheme', new_scheme)
