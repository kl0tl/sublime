import os, sublime, sublime_plugin, urllib, webbrowser

def load_settings():
  return sublime.load_settings('SearchOnline.sublime-settings')

def list_engines():
  settings = load_settings()
  engines = settings.get('engines', [])
  if settings.has('default_engine'):
    engines.append(settings.get('default_engine'))
  return sorted(engines, key = lambda engine: engine['name'].lower())

def format_disjunction(xs):
  if len(xs) == 0:
    return ''
  elif len(xs) == 1:
    return xs[0]
  else:
    init = [str(x) for x in xs[0:-1]]
    last = str(xs[-1])
    return ', '.join(init) + ' or %s' % last

def find_engine_by_name(name):
  engines = list_engines()
  engine = next((
    engine for engine in engines
      if engine['name'] == name
  ), None)
  if engine:
    return engine
  else:
    expected = format_disjunction([engine['name'] for engine in engines])
    msg = 'Unknown engine %s.\n\nExpected one of %s.' % (name, expected)
    raise Exception(msg)

def find_engines_by_scope(scope):
  settings = load_settings()
  engines = [
    engine for (score, engine) in sorted((
      (sublime.score_selector(scope, engine['selector']), engine)
        for engine in settings.get('engines', [])
          if 'selector' in engine
    ), key = lambda x: x[0]) if score > 0
  ]
  if len(engines) > 0:
    return engines
  elif settings.has('default_engine'):
    return [settings.get('default_engine')]
  else:
    msg = 'No engine matching scope\n\n%s\n\nRegister an engine for this scope or a default engine.' % scope.strip()
    raise Exception(msg)

class SearchOnlineCommand(sublime_plugin.TextCommand):
  def run(self, edit, engine = None):
    selection = self.view.sel()
    non_empty_regions = [region for region in selection if not region.empty()]
    queried_region = non_empty_regions[0] if len(non_empty_regions) > 0 else selection[0]
    try:
      if engine and engine != 'auto':
        self.search_at(queried_region, find_engine_by_name(engine))
      else:
        if engine == 'auto':
          scope = self.view.scope_name(queried_region.begin())
          engines = find_engines_by_scope(scope)
        else:
          engines = list_engines()
        if len(engines) == 1:
          self.search_at(queried_region, engines[0])
        else:
          on_done = lambda index: index > -1 and self.search_at(queried_region, engines[index])
          self.view.window().show_quick_panel([engine['name'] for engine in engines], on_done)
    except (Exception) as exception:
      sublime.error_message('Search Online: ' + str(exception))

  def search_at(self, region, engine):
    on_done = lambda query: webbrowser.open_new_tab(engine['url'] % urllib.parse.quote_plus(query, encoding = 'utf8'))
    if region.empty():
      caption = 'Search %s' % engine['name']
      self.view.window().show_input_panel(caption, '', on_done, None, None)
    else:
      on_done(self.view.substr(region))
