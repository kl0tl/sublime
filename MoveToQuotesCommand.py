import sublime, sublime_plugin

# Test cases:
#
# `view.run_command("move_to_quotes", { "expand": True })`
#   + With cursor at X, the command should select the string:
#       "Here is the X cursor"
#
#   + With cursor at X, the command should select the single quoted string:
#       "Here is 'the X cursor' now"
#
#   + With cursor at X, the command should select the double quoted string:
#       "Here the cursor is 'outside' the X selection"
#
# Without `expand` the command should move the cursor alternatively before the last and after the first quotes of the selected region

class MoveToQuotesCommand(sublime_plugin.TextCommand):
  def run(self, edit, expand = False):
    print(expand)

    d_quotes = list(map(lambda x: x.begin(), self.view.find_all('"')))
    s_quotes = list(map(lambda x: x.begin(), self.view.find_all("'")))

    for sel in self.view.sel():
      def search_for_quotes(q_type, quotes):
        q_size, before, after = False, False, False

        if len(quotes) - self.view.substr(sel).count('"') >= 2:
          all_before = list(filter(lambda x: x < sel.begin(), quotes))
          all_after = list(filter(lambda x: x >= sel.end(), quotes))

          if all_before: before = all_before[-1]
          if all_after: after = all_after[0]

          if all_before and all_after: q_size = after - before

        return q_size, before, after

      d_size, d_before, d_after = search_for_quotes('"', d_quotes)
      s_size, s_before, s_after = search_for_quotes("'", s_quotes)

      def replace_region(start, end):
        if sel.size() < end-start-2:
          start += 1; end -= 1
        self.view.sel().subtract(sel)
        if expand:
          self.view.sel().add(sublime.Region(start, end))
        else:
          pos = start if sel.end() == end else end
          self.view.sel().add(sublime.Region(pos, pos))

      if d_size and (not s_size or d_size < s_size):
        replace_region(d_before, d_after+1)
      elif s_size and (not d_size or s_size < d_size):
        replace_region(s_before, s_after+1)
