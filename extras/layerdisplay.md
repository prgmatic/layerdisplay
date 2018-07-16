---
layout: plugin

id: layerdisplay
title: LayerDisplay
description: Displays the current layer and total layers for a print job.
author: Matt Thompson
license: AGPLv3

date: 2018-07-15

homepage: https://github.com/chatrat12/layerdisplay
source: https://github.com/chatrat12/layerdisplay
archive: https://github.com/chatrat12/layerdisplay/archive/master.zip

tags:
- layer
- display
- progress


screenshots:
- url: https://i.imgur.com/v0PFLbV.png
  alt: Screenshot
  caption: Layer info displayed in OctoPrint.
- ...

# TODO
featuredimage: https://i.imgur.com/v0PFLbV.png

---

# LayerDisplay

Plugin for Octoprint that displays what layer a print job is on.

LayerDisplay does not require special GCode comments. LayerDisplay analyzes the GCode before the a print starts to figure out where layer changes happen. LayerDisplay does not work when printing from the SD card.
