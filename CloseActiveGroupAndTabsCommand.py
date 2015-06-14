import sublime_plugin

class CloseActiveGroupAndTabsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    window = self.view.window()

    # For some reasons an error is thrown when `run_multiple_commands` tries to run `destroy_pane` after `close_all_in_active_group`

    window.run_command('close_all_in_active_group')
    window.run_command('destroy_pane', { 'direction': 'self' })
