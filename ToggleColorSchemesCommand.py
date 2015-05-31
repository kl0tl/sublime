import os.path
import sublime, sublime_plugin

class ToggleColorSchemesCommand(sublime_plugin.TextCommand):

  def run(self, edit, color_schemes):
    expanded = [self.expand(color_scheme) for color_scheme in color_schemes]

    for color_scheme in expanded:
      self.save(color_scheme)

    for view in sublime.active_window().views():
        self.update_views(view, expanded)

  def expand(self, color_scheme):
    settings_path = color_scheme.get('settings')
    settings = sublime.load_settings(settings_path)

    light_scheme = color_scheme.get('light')
    dark_scheme = color_scheme.get('dark')

    current_scheme = settings.get('color_scheme')
    new_scheme = dark_scheme if (current_scheme == light_scheme) else light_scheme

    scopes = color_scheme.get('scopes', [])

    return {
      'settings': settings,
      'settings_path': settings_path,
      'color_scheme': new_scheme,
      'scopes': scopes
    }

  def save(self, expanded):
    settings = expanded.get('settings')
    settings_path = expanded.get('settings_path')
    color_scheme = expanded.get('color_scheme')

    settings.set('color_scheme', color_scheme)
    sublime.save_settings(settings_path)

  def update_views(self, view, color_schemes):
    best_score = -1
    best_candidate = None

    for color_scheme in color_schemes:
      for scope in color_scheme.get('scopes'):
        score = view.score_selector(0, scope)
        if score > best_score:
          best_score = score
          best_candidate = color_scheme

    if best_candidate:
      view.settings().set('color_scheme', best_candidate.get('color_scheme'))
