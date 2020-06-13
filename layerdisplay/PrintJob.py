import os
from .GCodeAnalyzer import GCodeAnalyzer
from .Event import Event
from threading import Thread, Timer
import threading

class PrintJob:

	layer_change_info = None
	on_layer_change = Event()
	on_analysis_complete = Event()
	printing = False
	file_size = -1


	def __init__(self, file_path, is_local):
		self.file_path = file_path
		self.file_name = os.path.basename(self.file_path)
		self.local = is_local

		if self.local:
			self.file_size = os.path.getsize(self.file_path)
			self._start_analysis(self.file_path)
		self.current_layer = 0


	def started(self):
		self.current_layer = 0
		self.printing = True

	def stopped(self):
		self.printing = False

	def get_layer_count(self):
		return self.layer_change_info.get_layer_count()

	def is_analysing_gcode(self):
		return self._gcode_analyzer and self._gcode_analyzer.is_working()

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

	def _start_analysis(self, file_path):
		self._gcode_analyzer = GCodeAnalyzer()
		self._gcode_analyzer.prepare_for_job()
		def do_analysis():
			gcode = file(file_path, "r")
			fileSize = os.path.getsize(file_path)
			self.layer_change_info = self._gcode_analyzer.get_print_job_layer_information(gcode, self.file_size)
			self.on_analysis_complete.invoke()

		analysis_thread = Thread(target=do_analysis)
		analysis_thread.start()

	def to_string(self):
		if self._gcode_analyzer and self._gcode_analyzer.is_working():
			file_pos = float(self._gcode_analyzer.get_current_file_position())
			return "Analysing: %%%.1f" %  (file_pos / self.file_size * 100)
		elif self.layer_change_info:
			if self.printing:
				return "%d / %d" % (self.current_layer + 1, self.get_layer_count())
			else:
				return "- / %d" % self.get_layer_count()
		return "-"

