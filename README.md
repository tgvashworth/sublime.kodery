# Kodery for Sublime Text

**Note:** This plugin is in the early stages of development and may be unstable or cause Sublime Text to be slow or crash entirely. You have been warned.

## Install

Clone the repository into your Sublime Packages folder, or download a zip. On OSX, that's `~/Library/Application Support/Sublime Text 2/Packages/`.


```
git clone https://github.com/phuu/sublime.kodery.git
```

We'll be on the Sublime Package Control soon.

## Usage

To use the plugin, there's a few steps to take:

1. Generate yourself an access token. Head to [account.kodery.com](http://account.kodery.com) and sign in. You'll see a token generation tool there. Name it something nice, like [Sublime Plugin].
2. Tell Sublime about your token. Add some JSON to your Sublime Preferences (`cmd+,` on a Mac):

```json
"kodery": {
  "token": "6b3a55e0261b0304143f805a24924d0c1c44524821305f31d9277843b8a10f4e"
}
```
3. Use the Sublime Command Palette to reload your snippets! Open it up (`cmd+shift+p` for me) and type "kodery reload". You'll see it.

All being well, you'll see "Your Kodery snippets were reloaded" in the Sublime's status bar.

If you don't, and you get an error, [tweet me](http://twitter.com/phuunet).

## Gotchas

Sublime supports a `$` syntax for snippet replacement syntax, which mean it'll try to replace your PHP variables and jQuery plugins. We're working on this, but, for now, stick a `\` before the important `$` signs in your snippets.

## License

MIT