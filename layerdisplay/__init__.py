# coding=utf-8
from __future__ import absolute_import

import os
import octoprint.plugin
from octoprint.events import Events
from layerdisplay.GCodeAnalyzer import GCodeAnalyzer

class LayerDisplayPlugin(octoprint.plugin.StartupPlugin,
					     octoprint.plugin.EventHandlerPlugin,
					     octoprint.plugin.AssetPlugin,
					     octoprint.printer.PrinterCallback):

	def on_after_startup(self):
		self._analyzer = GCodeAnalyzer()
		self._printing = False
		self._fileSelected = False
		self._fileRead = False

	def on_event(self, event, payload):
		if event == Events.FILE_SELECTED:
			# Can't analyze gcode on sd card.
			if payload['origin'] != 'local':
				return
			self._fileRead = True
			self._fileSelected = True
			self.__analyzeGCode(payload['file'])
			self.updateCurrentLayerString();

		elif event == Events.FILE_DESELECTED:
			self._fileSelected = False
			self._fileRead = False
			self.updateCurrentLayerString();

		elif event == Events.PRINT_STARTED:
			self._currentLayer = 1
			self._printing = True
			self._printer.register_callback(self)
			self.updateCurrentLayerString();
			
		elif event == Events.PRINT_CANCELLED or event == Events.PRINT_DONE or event == Events.PRINT_FAILED:
			self._printing = False
			self._printer.unregister_callback(self)
			self.updateCurrentLayerString();

	def __analyzeGCode(self, filePath):
		gcode = file(filePath, "r")
		fileSize = os.path.getsize(filePath)
		self._analyzer.analyze_gcode(gcode, fileSize)
		self._logger.info("%d layers in gcode" % self._analyzer.getLayerCount())

	def on_printer_send_current_data(self, data):
		if data['state']['flags']['printing'] and self._fileRead:
			totalLayers = self._analyzer.getLayerCount()
			if self._currentLayer < totalLayers:
				nextLinePercentage = self._analyzer.getLayerChangePositions()[self._currentLayer]
				percentage = data['progress']['completion'] / 100
				while percentage >= nextLinePercentage and self._currentLayer < totalLayers:
					self._currentLayer += 1
					self.updateCurrentLayerString()
					if self._currentLayer < totalLayers:
						nextLinePercentage = self._analyzer.getLayerChangePositions()[self._currentLayer]

	def updateCurrentLayerString(self):
		result = "-"
		if self._fileRead:
			if self._printing:
				result = "%d / %d" % (self._currentLayer, self._analyzer.getLayerCount())
			elif self._fileSelected:
				result = "- / %d" % self._analyzer.getLayerCount()
		self._plugin_manager.send_plugin_message(self._plugin_name, dict(layerString = result))


	def get_assets(self):
		return dict(js=["js/LayerDisplay.js"])

	def get_update_information(self):
		return dict(
			layerdisplay=dict(
				displayName=self._plugin_name,
				displayVersion=self._plugin_version,

				type="github_release",
				current=self._plugin_version,
				user="chatrat12",
				repo="LayerDisplay",

				pip="https://github.com/chatrat12/layerdisplay/archive/{target_version}.zip"
			)
		)

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = LayerDisplayPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
