import sublime, sublime_plugin

# 'let\'s go !'

# a = 'test'
# b = "This shouldn't break"

# ‘abc’
# “abc”
# ‹abc›
# «abc»
# <abc>
# 'abc'
# "abc"
# '''abc'''
# """abc""""
# `abc` 
# (    )
# {    }
# [    ]

"""

"""

class MoveToQuotesCommand(sublime_plugin.TextCommand):
  def run(self, edit, expand = False):
    settings = sublime.load_settings('MoveToQuotes.sublime-settings')
    pairs = map(lambda pair: Pair(
      OpeningQuote(pair.get('opening_quote', ''), pair.get('opening_scope', None)),
      EndingQuote(pair.get('ending_quote', ''), pair.get('ending_scope', None)),
      pair.get('scope', None)
    ), settings.get('pairs'))

    for caret in self.view.sel():
      expanded = map(lambda pair: self.expand_to_quotes(caret, pair, expand), pairs)
      filtered = filter(lambda x: x, expanded)

      # `min()` throw if `filtered` is empty :(

      min_offset = float('inf')
      pos = None

      for a, b in filtered:
        offset = b - a
        if offset < min_offset:
          min_offset = offset
          pos = a, b

      if pos:
        start, end = pos
        self.move_caret_to(caret, start if expand else end, end)

  def expand_to_quotes(self, region, pair, expand):
    left = Parser(self.view, region.a)
    right = Parser(self.view, region.b)

    # if region.b < region.a:
    #   left, right = right, left

    right_quoted = right.is_quoted(pair)

    if right_quoted:
      enclosing_region = None
    else:
      settings = self.view.settings()

      if not settings.has('cached_quotes'):
        settings.set('cached_quotes', {})

      cache = settings.get('cached_quotes')
      pattern = pair.pattern()

      if pattern:
        if pattern in cache:
          regions = cache.get(pattern)
        else:
          regions = cache[pattern] = self.view.find_all(pair.pattern())

        enclosing_region = next(filter(lambda region: region.contains(right.pos), regions), None)
      else:
        enclosing_region = None

    left_after_opening_quote = left.is_after_opening_quote(pair.opening, enclosing_region)
    right_before_ending_quote = right.is_before_ending_quote(pair.ending, enclosing_region)

    if expand and left_after_opening_quote and right_before_ending_quote:
      start = left.move_before_opening_quote(pair.opening, enclosing_region)
      end = right.move_after_ending_quote(pair.ending, enclosing_region)
      return (start, end)

    left_before_opening_quote = left.is_before_opening_quote(pair.opening, enclosing_region)
    right_after_ending_quote = right.is_after_ending_quote(pair.ending, enclosing_region)

    if expand and left_before_opening_quote and right_after_ending_quote:
      return (left.pos, right.pos)

    if expand and left_before_opening_quote and right_quoted:
      end = right.move_after_ending_quote(pair.ending, enclosing_region)
      return (left.pos, end)

    left_quoted = left.is_quoted(pair)

    if expand and right_after_ending_quote and left_quoted:
      start = right.move_before_opening_quote(pair.opening, enclosing_region)
      return (start, left.pos)

    # print('expand_to_quotes')
    # print('  ', pair.opening.char, pair.ending.char)
    # print('  ', left.pos, right.pos)
    # print('  quoted ?', is_quoted)
    # print('  enclosing_region ? ', enclosing_region)

    right_before_opening_quote = right.is_before_opening_quote(pair.opening, enclosing_region)
    right_after_opening_quote = right.is_after_opening_quote(pair.opening, enclosing_region)

    if right_before_opening_quote:
      # print('before', pair.opening.char, '(opening)')
      end = right.move_after_ending_quote(pair.ending, enclosing_region)
      return (left.pos, end)

    if right_after_opening_quote:
      # print('after', pair.opening.char, '(opening)')
      end = right.move_before_ending_quote(pair.ending, enclosing_region)
      return (left.pos, end)

    if right_before_ending_quote:
      # print('before', pair.ending.char, '(ending)')
      end = right.move_after_opening_quote(pair.opening, enclosing_region)
      return (left.pos, end)

    if right_after_ending_quote:
      # print('after', pair.ending.char, '(ending)')
      end = right.move_before_opening_quote(pair.opening, enclosing_region)
      return (left.pos, end)

    if right_quoted or enclosing_region:
      start = left.move_after_opening_quote(pair.opening, enclosing_region)
      end = right.move_before_ending_quote(pair.ending, enclosing_region)
      return (start, end)

    return None

  def move_caret_to(self, caret, start, end):
    regions = self.view.sel()
    regions.subtract(caret)
    regions.add(sublime.Region(start, end))


class CachedQuotesEventListener(sublime_plugin.EventListener):
  def on_modified(self, view):
    settings = view.settings()
    if settings.has('cached_quotes'):
      settings.get('cached_quotes').clear()


class Quote:
  def __init__(self, char, scope = None):
    self.char = char
    self.scope = scope

  def is_empty(self):
    return self.size() == 0

  def size(self):
    return len(self.char)


class OpeningQuote(Quote):
  pass


class EndingQuote(Quote):
  pass


class Pair:
  def __init__(self, opening, ending, scope = None):
    self.opening = opening
    self.ending = ending
    self.scope = scope

  def pattern(self):
    empty = self.opening.is_empty() or self.ending.is_empty()
    return None if empty else self.opening.char + '[^' + self.ending.char[0] + ']*' + self.ending.char


class Parser:
  def __init__(self, view, pos = 0):
    self.view = view
    self.pos = pos

  def is_before_opening_quote(self, quote, enclosing_region = None):
    if quote.scope:
      return self.matches(quote.scope)
    if quote.is_empty:
      return False
    return self.is_before(quote) and enclosing_region.begin() == self.pos

  def is_after_opening_quote(self, quote, enclosing_region = None):
    if quote.scope:
      return self.matches_at(self.pos - 1, quote.scope)
    if quote.is_empty():
      return False
    return self.is_after(quote) and self.pos - enclosing_region.begin() == quote.size()

  def is_before_ending_quote(self, quote, enclosing_region = None):
    if quote.scope:
      return self.matches(quote.scope)
    if quote.is_empty():
      return False
    return self.is_before(quote) and enclosing_region.end() - self.pos == quote.size()

  def is_after_ending_quote(self, quote, enclosing_region = None):
    if quote.scope:
      return self.matches_at(self.pos - 1, quote.scope)
    if quote.is_empty():
      return False
    return self.is_after(quote) and enclosing_region.end() == self.pos

  def is_before(self, quote):
    region = sublime.Region(self.pos, self.pos + quote.size())
    return self.view.substr(region) == quote.char

  def is_after(self, quote):
    region = sublime.Region(self.pos - quote.size(), self.pos)
    return self.view.substr(region) == quote.char

  def is_quoted(self, pair):
    return pair.scope and self.matches(pair.scope)

  def matches(self, scope):
    return self.matches_at(self.pos, scope)

  def matches_at(self, pos, scope):
    return self.view.score_selector(pos, scope) > 0

  def move_before_opening_quote(self, quote, enclosing_region = None):
    return self.move_until(self.prev, lambda: self.is_before_opening_quote(quote, enclosing_region))

  def move_after_opening_quote(self, quote, enclosing_region = None):
    return self.move_until(self.prev, lambda: self.is_after_opening_quote(quote, enclosing_region))

  def move_before_ending_quote(self, quote, enclosing_region = None):
    return self.move_until(self.next, lambda: self.is_before_ending_quote(quote, enclosing_region))

  def move_after_ending_quote(self, quote, enclosing_region = None):
    return self.move_until(self.next, lambda: self.is_after_ending_quote(quote, enclosing_region))

  def move_until(self, step, predicate):
    while True:
      if predicate() or not step():
        break
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
