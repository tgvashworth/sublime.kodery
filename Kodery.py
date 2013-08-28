import sublime, sublime_plugin

import json
from urllib import urlopen


class Kodery(sublime_plugin.EventListener):
  url = "http://api.kodery.com/me/snippets?access_token="
  completions = []

  @staticmethod
  def reload():
    sublime.status_message('Reloading Kodery snippets...')

    # Load the current settings
    settings = sublime.load_settings("Preferences.sublime-settings").get('kodery', {})

    # If the token is missing, warn and quit.
    if 'token' not in settings:
      sublime.status_message('You are missing a Kodery token in your Sublime preferences.')
      return

    # Try to load the snippets, and warn if something goes wrong
    try:
      snippets = json.loads(urlopen(Kodery.url + settings.get('token', "")).read())
    except IOError:
      sublime.status_message('Your Kodery token is not valid. Generate a new one at account.kodery.com.')
      return

    # Build a list of fragments
    completions = []
    for snippet in snippets:
      # Append the completion with all fragments using the snippet name
      # completions.append({
      #   'name': snippet['name'],
      #   'description': snippet['category']['name'],
      #   'body': '\n\n'.join([fragment['body'] for fragment in snippet['fragments']])
      # })

      # Add individual fragments as completions
      for fragment in snippet['fragments']:
        if not fragment['name']:
          if len(snippet['fragments']) == 1:
            fragment['name'] = snippet['name']
          else:
            continue
        # Append the completion
        completions.append({
          'name': fragment['name'],
          'description': snippet['name'],
          'body': fragment['body']
        })

    # Save the completions as static class property
    Kodery.completions = completions

    sublime.status_message('Your Kodery were snippets reloaded.')

  def __init__(self):
    Kodery.reload()

  def on_query_completions(self, view, prefix, locations):
    # Find the matching completions and pass them back
    completions = []
    for completion in Kodery.completions:
      if completion['name'].lower().startswith(prefix.lower()):
        trigger = completion['name'] + '\t' + completion['description']
        completions.append((trigger, completion['body']))
    return completions

class ReloadKoderySnippetsCommand(sublime_plugin.WindowCommand):
  def run(self):
    Kodery.reload()
