import sublime, sublime_plugin

class MoveToQuotesCommand(sublime_plugin.TextCommand):
  def run(self, edit, expand = False):
    for sel in self.view.sel():
      left_parser = Parser(self.view, sel.begin())
      right_parser = Parser(self.view, sel.end())

      if expand and left_parser.is_after_begin_quote() and right_parser.is_before_end_quote():
        self.move_cursor(sel, left_parser.move_before_begin_quote(), right_parser.move_after_end_quote())
      elif not (expand and left_parser.is_before_begin_quote() and right_parser.is_after_end_quote()):
        if sel.b < sel.a:
          left_parser, right_parser = right_parser, left_parser

        if right_parser.is_before_begin_quote():
          right_parser.move_after_end_quote()
        elif right_parser.is_after_begin_quote():
          right_parser.move_before_end_quote()
        elif right_parser.is_before_end_quote():
          right_parser.move_after_begin_quote()
        elif right_parser.is_after_end_quote():
          right_parser.move_before_begin_quote()
        elif right_parser.is_quoted():
          left_parser.move_after_begin_quote()
          right_parser.move_before_end_quote()

        start = left_parser.pos
        end = right_parser.pos

        self.move_cursor(sel, start if expand else end, end)

  def move_cursor(self, cursor, start, end):
    regions = self.view.sel()
    regions.subtract(cursor)
    regions.add(sublime.Region(start, end))

class Parser:
  def __init__(self, view, pos = 0):
    self.view = view
    self.pos = pos
    self.begin_quote_scopes = [
      'punctuation.definition.string.begin',
      'punctuation.definition.quasi.begin'
    ]
    self.end_quote_scopes = [
      'punctuation.definition.string.end',
      'punctuation.definition.quasi.end'
    ]
    self.quoted_scopes = [
      'string.quoted',
      'string.quasi'
    ]

  def is_before_begin_quote(self):
    return self.matches(self.begin_quote_scopes)

  def is_after_begin_quote(self):
    return self.matches_at(self.pos - 1, self.begin_quote_scopes)

  def is_before_end_quote(self):
    return self.matches(self.end_quote_scopes)

  def is_after_end_quote(self):
    return self.matches_at(self.pos - 1, self.end_quote_scopes)

  def is_quoted(self):
    return self.matches(self.quoted_scopes)

  def matches(self, scopes):
    return self.matches_at(self.pos, scopes)

  def matches_at(self, pos, scopes):
    return any(map(lambda scope: self.view.score_selector(pos, scope) > 0, scopes))

  def move_before_end_quote(self):
    return self.move(self.next, self.is_before_end_quote)

  def move_after_end_quote(self):
    return self.move(self.next, self.is_after_end_quote)

  def move_before_begin_quote(self):
    return self.move(self.prev, self.is_before_begin_quote)

  def move_after_begin_quote(self):
    return self.move(self.prev, self.is_after_begin_quote)

  def move(self, step, predicate):
    while True:
      if predicate():
        break
      else:
        step()
    return self.pos

  def prev(self):
    if self.pos > 0:
      self.pos -= 1
      return True
    else:
      return False

  def next(self):
    if self.pos < self.view.size():
      self.pos += 1
      return True
    else:
      return False
