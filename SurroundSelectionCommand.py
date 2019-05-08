import sublime, sublime_plugin

def is_pair(a, b):
  return any(a == opening and b == closing for (opening, closing) in [
    ('(', ')'),
    ('[', ']'),
    ('{', '}'),
    ('<', '>'),
    ('‹', '›'),
    ('«', '»'),
    ('\'', '\''),
    ('"', '"'),
    ('‘', '’'),
    ('“', '”')
  ])

class SurroundSelectionCommand(sublime_plugin.TextCommand):
  def run(self, edit, skip_pairs = False):
    view = self.view
    sel = view.sel()
    for region in sel:
      if not region.empty():
        begin = region.begin()
        end = region.end()
        sel.subtract(region)
        if skip_pairs and is_pair(view.substr(begin), view.substr(end - 1)):
          begin += 1
          end -= 1
        sel.add(sublime.Region(begin, begin))
        sel.add(sublime.Region(end, end))
