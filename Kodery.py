import sublime, sublime_plugin

import json
from urllib import urlopen

kodery_url = "http://api.kodery.com/me/snippets?access_token="

class Kodery(sublime_plugin.EventListener):
  fragments = []

  @staticmethod
  def reload():
    sublime.status_message('Reloading Kodery snippets...')

    # Load the current settings
    settings = sublime.load_settings("Preferences.sublime-settings")
    kodery = settings.get('kodery', {})

    # If the token is missing, warn and quit.
    if 'token' not in kodery:
      sublime.status_message('You are missing a Kodery token in your Sublime preferences.')
      return

    # Try to load the snippets, and warn if something goes wrong
    try:
      snippets = json.loads(urlopen(kodery_url + kodery.get('token', "")).read())
    except IOError:
      sublime.status_message('Your Kodery token is not valid. Generate a new one at account.kodery.com.')
      return

    # Build a list of fragments
    fragments = []
    for snippet in snippets:
      for fragment in snippet['fragments']:
        if not fragment['name'] and len(snippet['fragments']) == 1:
          fragment['name'] = snippet['name']
        fragment['snippet'] = snippet
        fragments.append(fragment)
    Kodery.fragments = fragments

    sublime.status_message('Kodery snippets reloaded.')

  def __init__(self):
    Kodery.reload()

  def on_query_completions(self, view, prefix, locations):
    # Find the matching fragments and pass them back
    fragments = []
    for fragment in Kodery.fragments:
      if fragment['name'].lower().startswith(prefix.lower()):
        trigger = fragment['name'] + '\t' + fragment['snippet']['name']
        fragments.append((trigger, fragment['body']))
    return fragments

class ReloadKoderySnippetsCommand(sublime_plugin.WindowCommand):
  def run(self):
    Kodery.reload()
