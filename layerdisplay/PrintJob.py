import os
import GCodeAnalyzer
from Event import Event

class PrintJob:

	layer_change_info = None
	on_layer_change = Event()
	printing = False

	
	def __init__(self, file_selected_payload):
		self.file_name = file_selected_payload['name']
		self.local = file_selected_payload['origin'] == 'local'

		if self.local:
			self.layer_change_info = self._get_layer_info(file_selected_payload['file'])
		self.current_layer = 1

	
	def started(self):
		self.current_layer = 1
		self.printing = True

	def stopped(self):
		self.printing = False

	def get_layer_count(self):
		return self.layer_change_info.get_layer_count()

	def set_progress(self, progress):
		# Verify printing from octoprint and layer change info is available
		if self.local and self.layer_change_info != None:
			# Take note of the current layer, used layer to trigger the on_layer_change event.
			prev_layer = self.current_layer
			layer_count = self.layer_change_info.get_layer_count()

			# Only proceed if not already on final layer
			if self.current_layer < layer_count:
				next_layer_progress = self.layer_change_info.get_layer_change_position(self.current_layer)
				# If our progress is greater than the next layer point, increment the current layer
				while progress >= next_layer_progress and self.current_layer < layer_count:
					self.current_layer += 1
					next_layer_progress = self.layer_change_info.get_layer_change_position(self.current_layer)

			# if the layer has changed notify listeners
			if self.current_layer != prev_layer:
				self.on_layer_change.invoke()

	def _get_layer_info(self, file_path):
		gcode = file(file_path, "r")
		fileSize = os.path.getsize(file_path)
		return GCodeAnalyzer.get_print_job_layer_information(gcode, fileSize)

