class PositioningMode:
	absolute = 0
	relative = 1

class StepperTracker:

	_absolute_position = 0
	_previous_absolute_position = 0

	_input_mode = PositioningMode.absolute

	
	def get_absolute_position(self):
		return self._absolute_position
	def get_previous_absolute_position(self):
		return self._previous_absolute_position

	def set_position(self, new_position):
		self._previous_absolute_position = self._absolute_position
		if self._input_mode == PositioningMode.absolute:
			self._absolute_position = new_position
		else:
			self._absolute_position += new_position

	def get_positioning_mode(self):
		return _input_mode
	def set_positioning_mode(self, new_mode):
		self._input_mode = new_mode


