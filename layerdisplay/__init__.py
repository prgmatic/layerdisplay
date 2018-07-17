# coding=utf-8
from __future__ import absolute_import

import os
import octoprint.plugin
import layerdisplay.UpdateInfo
import layerdisplay.LayerInfoPusher
from octoprint.events import Events
from layerdisplay.PrintJob import PrintJob

class LayerDisplayPlugin(octoprint.plugin.EventHandlerPlugin,
					     octoprint.plugin.AssetPlugin,
					     octoprint.printer.PrinterCallback):

	print_job = None

	def on_event(self, event, payload):
		if event == Events.FILE_SELECTED:
			self.print_job = PrintJob(payload)
			self.print_job.on_layer_change.register_callback(self.on_layer_change)
			self.push_current_layer();

		elif event == Events.FILE_DESELECTED:
			self.print_job = None
			self.push_current_layer();

		elif event == Events.PRINT_STARTED:
			if self.print_job:
				self.print_job.started()
			self._printer.register_callback(self)
			self.push_current_layer();
			
		elif event == Events.PRINT_CANCELLED or event == Events.PRINT_DONE or event == Events.PRINT_FAILED:
			if self.print_job:
				self.print_job.stopped()
			self._printer.unregister_callback(self)
			self.push_current_layer();

	def on_printer_send_current_data(self, data):
		if data['state']['flags']['printing'] and self.print_job != None:
			progress = data['progress']['completion'] / 100
			self.print_job.set_progress(progress)

	def on_layer_change(self):
		self.push_current_layer()

	def push_current_layer(self):
		LayerInfoPusher.push(self, self.print_job)

	def get_assets(self):
		return dict(js=["js/LayerDisplay.js"])

	def get_update_information(self):
		return UpdateInfo.get_update_information(self)

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = LayerDisplayPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
