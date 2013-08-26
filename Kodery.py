import sublime, sublime_plugin

import json
from urllib import urlopen

kodery_url = "http://api.kodery.com/me/snippets?access_token="

class Kodery(sublime_plugin.EventListener):
  def __init__(self):
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
    self.fragments = []
    for snippet in snippets:
      for fragment in snippet['fragments']:
        self.fragments.append(fragment)

  def on_query_completions(self, view, prefix, locations):
    # Find the matching fragments and pass them back
    return [(fragment['name'], fragment['body']) for fragment in self.fragments if fragment['name'].startswith(prefix)]