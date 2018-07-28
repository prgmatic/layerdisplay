# LayerDisplay

Plugin for Octoprint that displays what layer a print job is on.

![Screenshot](https://i.imgur.com/v0PFLbV.png)

- **Does not require special GCode comments.** LayerDisplay analyzes the GCode before the a print starts to figure out where layer changes happen.
- *LayerDisplay does not work when printing from the SD card.*

## Installation

Install via the bundled [Plugin Manager](http://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html) or manually using this URL:

    https://github.com/chatrat12/layerdisplay/archive/master.zip
    
## TODO
- **Error checking** Handle any possible errors (such as read errors) and report them to the user.

## Feedback
This is my first python project. I don't know enough about python to follow my usual design patterns. Feedback is greatly apperciated :)
