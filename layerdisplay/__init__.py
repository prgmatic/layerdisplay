# coding=utf-8
from __future__ import absolute_import

import os
import octoprint.plugin
import layerdisplay.UpdateInfo
import layerdisplay.LayerInfoPusher
from octoprint.events import Events
from layerdisplay.PrintJob import PrintJob
from threading import Timer

class LayerDisplayPlugin(octoprint.plugin.EventHandlerPlugin,
					     octoprint.plugin.AssetPlugin,
						 octoprint.plugin.SimpleApiPlugin,
					     octoprint.printer.PrinterCallback):

	print_job = None

	def on_event(self, event, payload):
		if event == Events.FILE_SELECTED:
			is_local = payload.get('origin') == 'local'
			file_path = self._file_manager.path_on_disk(payload.get("origin"), payload.get("path"))
			self.print_job = PrintJob(file_path, is_local)
			if self.print_job.is_analysing_gcode():
				self.send_analysis_progress_updates()
				self.print_job.on_analysis_complete.register_callback(self.push_layer_info)
			self.print_job.on_layer_change.register_callback(self.push_layer_info)
			self.push_layer_info()

		elif event == Events.FILE_DESELECTED:
			self.print_job = None
			self.push_layer_info()

		elif event == Events.PRINT_STARTED:
			if self.print_job:
				self.print_job.started()
			self._printer.register_callback(self)
			self.push_layer_info()
			
		elif event == Events.PRINT_CANCELLED or event == Events.PRINT_DONE or event == Events.PRINT_FAILED:
			if self.print_job:
				self.print_job.stopped()
			self._printer.unregister_callback(self)
			self.push_layer_info()

	def on_printer_send_current_data(self, data):
		if data['state']['flags']['printing'] and self.print_job != None:
			progress = data['progress']['completion'] / 100
			self.print_job.set_progress(progress)

	def send_analysis_progress_updates(self):
		if self.print_job and self.print_job.is_analysing_gcode():
			Timer(0.5, self.send_analysis_progress_updates).start()
			self.push_layer_info()

	def push_layer_info(self):
		LayerInfoPusher.push(self, self.print_job)

	def get_assets(self):
		return dict(js=["js/LayerDisplay.js"])

	def get_update_information(self):
		return UpdateInfo.get_update_information(self)

	# SimpleApiPlugin
	def on_api_get(self, request):
		import flask
		result = LayerInfoPusher.get_layer_info_string(self.print_job)
		return flask.jsonify(layerString = result)

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = LayerDisplayPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
