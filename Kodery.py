import sublime, sublime_plugin
import threading

import json
import urllib2

class KoderyApiCall(threading.Thread):
  def __init__(self, url):
    threading.Thread.__init__(self)
    self.url = url
    self.result = None

  def run(self):
    # Hit the Kodery API, and hope nothing goes wrong!
    try:
      self.result = json.loads(urllib2.urlopen(self.url).read())
      return
    # Well, ok, handle some errors.
    except (urllib2.HTTPError) as (e):
      err = '%s encountered a %s HTTP Error when contacting the API. Sorry.' % (__name__, str(e.code))
    except (urllib2.URLError) as (e):
      err = '%s encountered an error (%s) when contacting the Kodery API. Sorry.' % (str(e.reason))
    except IOError:
      err = 'Your Kodery token is not valid. Generate a new one at account.kodery.com.'
    else:
      err = 'Something went wrong while reloading your Kodery snippets. Sorry.'

    # Tell the user
    sublime.error_message(err)

class Kodery(sublime_plugin.EventListener):
  def __init__(self):
    Kodery.reload()

  url = "http://api.kodery.com/me/snippets?source=sublime&access_token="
  completions = []

  @staticmethod
  def thread_finished(thread):
    # Thread finished running, but was it successful?
    if thread.result == None:
      return

    # Grab out that result
    snippets = thread.result

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

  @staticmethod
  def wait_for_thread(thread, done):
    # Check if the thread is still going. If it is, wait 100ms then try again
    if thread.is_alive():
      sublime.set_timeout(lambda: Kodery.wait_for_thread(thread, done), 100)
      return
    # Ooh, it is! Call the done callback.
    done(thread)

  @staticmethod
  def reload():
    sublime.status_message('Reloading Kodery snippets...')

    # Load the current settings
    settings = sublime.load_settings("Preferences.sublime-settings").get('kodery', {})

    # If the token is missing, warn and quit.
    if 'token' not in settings:
      sublime.status_message('You are missing a Kodery token in your Sublime preferences.')
      return

    # Try to load the snippets in a thread
    thread = KoderyApiCall(Kodery.url + settings.get('token', ""))
    thread.start()

    # Wait for the thread to be finished
    Kodery.wait_for_thread(thread, Kodery.thread_finished)

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
