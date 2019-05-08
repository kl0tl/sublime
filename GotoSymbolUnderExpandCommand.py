import sublime_plugin

def first(xs):
  return xs[0]


class GotoSymbolUnderExpandCommand(sublime_plugin.WindowCommand):
  def run(self):
    view = self.window.active_view()
    region = self.expand_region(view, first(view.sel()))
    symbol = self.region_to_symbol(view, region)
    self.show_overlay(symbol)

  def expand_region(self, view, region):
    return view.word(region) if region.empty() else region

  def region_to_symbol(self, view, region):
    return view.substr(region)

  def show_overlay(self, symbol):
    self.window.run_command('show_overlay', { 'overlay': 'goto', 'text': '@' + symbol })
